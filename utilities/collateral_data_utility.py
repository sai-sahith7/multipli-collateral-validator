import concurrent.futures
import os
import time

from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.middleware import ExtraDataToPOAMiddleware

from config import logger
from constants.chains.chain_base import ChainConstantsBaseClass
from constants.strategy_constants import StrategyConstants


class BlockchainClient:
    def __init__(self, chain_constants: ChainConstantsBaseClass):
        self.web3 = Web3(Web3.HTTPProvider(chain_constants.get_http_provider()))
        self.web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.contract_address = Web3.to_checksum_address(chain_constants.get_public_contract_address())
        self.chain_id = int(chain_constants.get_chain_id())
        self.wallet_address = Web3.to_checksum_address(os.getenv("WALLET_ADDRESS"))
        self.private_key = os.getenv("WALLET_PRIVATE_KEY")
        self.abi = chain_constants.get_abi_json()
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        self.chain_constants = chain_constants

    def __str__(self):
        return self.chain_constants.CHAIN_NAME

    def _fetch_events_in_chunk(self, event_name, start_block, end_block):
        """Fetch events within a specific block range."""
        try:
            event_filter = self.contract.events[event_name].create_filter(
                from_block=start_block, to_block=end_block
            )
            return event_filter.get_all_entries()
        except Exception as e:
            logger.info(
                f"Error fetching {event_name} events for blocks {start_block}-{end_block}: {str(e)}"
            )
            if end_block - start_block > 1000:
                logger.info(f"Subdividing chunk {start_block}-{end_block}")
                mid_block = (start_block + end_block) // 2
                time.sleep(1)

                left_result = self._fetch_events_in_chunk(
                    event_name, start_block, mid_block
                )
                right_result = self._fetch_events_in_chunk(
                    event_name, mid_block + 1, end_block
                )

                combined_results = list()
                if left_result:
                    combined_results.extend(left_result)
                if right_result:
                    combined_results.extend(right_result)
                return combined_results
            return list()

    def _process_chunk(self, chunk_range):
        start_block, end_block = chunk_range
        logger.info(f"Processing blocks {start_block} to {end_block}")

        events = list()

        data_push_events = self._fetch_events_in_chunk(
            event_name=self.chain_constants.EVENT_NAME,
            start_block=start_block,
            end_block=end_block
        )

        for event in data_push_events:
            if event['args']['submitter'].lower() == self.wallet_address.lower():
                events.append({
                    'block_number': event['blockNumber'],
                    'transaction_hash': event['transactionHash'].hex(),
                    'timestamp': self.web3.eth.get_block(event['blockNumber']).timestamp,
                    'submitter': event['args']['submitter'],
                    'collateralRatio': event['args']['collateralRatio'],
                    'event_timestamp': event['args']['timestamp'],
                    'info': event['args']['info']
                })

        return events

    def pre_transaction_check(self, hours=7, minutes=45):
        event_name = self.chain_constants.EVENT_NAME
        latest_block = self.web3.eth.block_number
        start_block = self.web3.eth.block_number - int(self.chain_constants.PAST_EVENT_LOOKUP_BLOCK_RANGE)
        chunk_size = self.chain_constants.CHUNK_SIZE

        events = list()

        num_chunks = (latest_block - start_block) // chunk_size + 1
        chunks = [
            (
                start_block + i * chunk_size,
                min(start_block + (i + 1) * chunk_size - 1, latest_block),
            )
            for i in range(num_chunks)
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_chunk = {
                executor.submit(self._process_chunk, chunk): chunk
                for chunk in chunks
            }

            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                result = future.result()
                if result:
                    events.extend(result)

        if not events:
            return True

        events.sort(key=lambda x: x['timestamp'], reverse=True)
        latest_event = events[0]

        current_time = int(time.time())
        time_since_last_push = current_time - latest_event['timestamp']

        threshold_seconds = (hours * 60 * 60) + (minutes * 60)

        return time_since_last_push >= threshold_seconds

    def get_collateral_ratio_decimals(self):
        return self.contract.functions.getCollateralRatioDecimals().call()

    def build_transaction(self, collateral_ratio, info_string):
        nonce = self.web3.eth.get_transaction_count(self.wallet_address)
        gas_price = self.web3.eth.gas_price

        return self.contract.functions.pushCollateralData(
            collateral_ratio,
            info_string
        ).build_transaction({
            'from': self.wallet_address,
            'gas': 100000,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': int(self.chain_id)
        })

    def sign_and_send_transaction(self, tx):
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash

    def wait_for_receipt(self, tx_hash):
        try:
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt.status == 1
        except TransactionNotFound:
            return False


class CollateralDataPusher:
    @classmethod
    def push_collateral_data(cls, blockchain_client, percentage: float, info_string: str) -> bool:
        decimals = blockchain_client.get_collateral_ratio_decimals()
        collateral_ratio = int(percentage * (10 ** decimals))
        tx = blockchain_client.build_transaction(collateral_ratio, info_string)
        tx_hash = blockchain_client.sign_and_send_transaction(tx)
        logger.info(f"Collateral Ratio: {collateral_ratio}")
        logger.info(f"Transaction Hash: {tx_hash}")
        return blockchain_client.wait_for_receipt(tx_hash)

    @classmethod
    def push_latest_collateral_data(cls):
        enabled_chain_constants = StrategyConstants.get_data_push_enabled_chain_constants_classes()

        if enabled_chain_constants is None:
            return False

        blockchain_clients = list()
        for chain_constants in enabled_chain_constants:
            blockchain_clients.append(BlockchainClient(chain_constants))

        valid_blockchain_clients = list()
        for blockchain_client in blockchain_clients:
            if blockchain_client.pre_transaction_check(hours=7, minutes=45) is True:
                valid_blockchain_clients.append(blockchain_client)
            else:
                logger.info(f"{blockchain_client}: Only one transaction is allowed in a time period of 8 hours.")

        if len(valid_blockchain_clients) == 0:
            return False

        strategy_class = StrategyConstants.get_strategy_class()
        percentage = strategy_class.execute()
        if percentage is None:
            return False
        info_string = strategy_class.__name__

        status_of_transactions = dict()
        for blockchain_client in valid_blockchain_clients:
            status_of_transactions[str(blockchain_client)] = cls.push_collateral_data(blockchain_client, percentage, info_string)

        return status_of_transactions