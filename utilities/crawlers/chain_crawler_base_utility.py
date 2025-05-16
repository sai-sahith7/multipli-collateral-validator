import concurrent.futures
import json
import time
from decimal import Decimal

from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

from config import logger
from utilities.market_price_utility import MarketPriceUtility


class BlockchainCrawlerBase:
    """Base class for blockchain crawlers that track deposit and withdrawal events."""

    CHAIN_NAME = None
    START_BLOCK = None
    DEFAULT_CHUNK_SIZE=None

    http_provider_url = None
    contract_address = None

    _deposit_balances = dict()
    _withdrawal_balances = dict()
    _final_balances = dict()
    _token_address_to_name = dict()
    _token_address_to_decimal = dict()
    _last_block = None

    _w3 = None
    _contract = None
    _token_info = None
    abi_json = None


    @classmethod
    def _initialize(cls):
        """Initialize Web3 and token mappings."""
        if cls._w3 is None:
            cls._initialize_web3(
                cls.http_provider_url, cls.contract_address, cls.abi_json
            )

            for token_name, token_info in cls._token_info.items():
                checksummed_address = Web3.to_checksum_address(token_info["address"])
                cls._token_address_to_name[checksummed_address] = token_name
                cls._token_address_to_decimal[checksummed_address] = token_info[
                    "decimal"
                ]


    @classmethod
    def _initialize_web3(cls, http_provider_url, contract_address, abi_json):
        """Initialize Web3 connection and contract."""
        cls._w3 = Web3(Web3.HTTPProvider(http_provider_url))
        cls._w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        if isinstance(abi_json, str):
            abi = json.loads(abi_json)
        else:
            abi = abi_json

        cls._contract = cls._w3.eth.contract(address=contract_address, abi=abi)

    @classmethod
    def _calculate_final_balances(cls):
        """Calculate final token balances by combining deposits and withdrawals."""
        return {
            token: Decimal(cls._deposit_balances.get(token, 0))
            + Decimal(cls._withdrawal_balances.get(token, 0))
            for token in set(cls._deposit_balances) | set(cls._withdrawal_balances)
        }

    @classmethod
    def _fetch_events_in_chunk(cls, event_name, start_block, end_block):
        """Fetch events within a specific block range."""
        cls._initialize()
        try:
            event_filter = cls._contract.events[event_name].create_filter(
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

                left_result = cls._fetch_events_in_chunk(
                    event_name, start_block, mid_block
                )
                right_result = cls._fetch_events_in_chunk(
                    event_name, mid_block + 1, end_block
                )

                combined_results = list()
                if left_result:
                    combined_results.extend(left_result)
                if right_result:
                    combined_results.extend(right_result)
                return combined_results
            return list()

    @classmethod
    def _process_chunk(cls, chunk_range):
        """Process a chunk of blocks for all events at once."""
        start_block, end_block = chunk_range
        logger.info(f"Processing blocks {start_block} to {end_block}")

        deposits = list()
        withdrawals = list()

        deposit_events = cls._fetch_events_in_chunk(
            "BridgedDeposit", start_block, end_block
        )
        for event in deposit_events:
            token_address = event.args.token
            if token_address in cls._token_address_to_name:
                token_name = cls._token_address_to_name[token_address]
                decimal = cls._token_address_to_decimal[token_address]

                deposits.append(
                    {
                        "token": token_name,
                        "amount": Decimal(event.args.amount) / Decimal(10**decimal),
                        "user": event.args.user,
                    }
                )

        withdrawal_events = cls._fetch_events_in_chunk(
            "BridgedWithdrawal", start_block, end_block
        )
        for event in withdrawal_events:
            token_address = event.args.token
            if token_address in cls._token_address_to_name:
                token_name = cls._token_address_to_name[token_address]
                decimal = cls._token_address_to_decimal[token_address]

                withdrawals.append(
                    {
                        "token": token_name,
                        "amount": Decimal(event.args.amount) / Decimal(10**decimal),
                        "user": event.args.user,
                    }
                )

        logger.info(
            f"Found {len(deposit_events)} deposits and {len(withdrawal_events)} withdrawals in blocks {start_block}-{end_block}"
        )
        return {"deposits": deposits, "withdrawals": withdrawals}

    @classmethod
    def _process_events(cls, events_data, is_withdrawal=False):
        """Process deposit or withdrawal events and calculate token balances."""
        token_balances = dict()

        for event in events_data:
            token_name = event["token"]
            amount = event["amount"]

            token_balances[token_name] = token_balances.get(token_name, 0) + (
                -amount if is_withdrawal else amount
            )

        return token_balances

    @classmethod
    def _run_crawler(cls, start_block=None, num_workers=10, chunk_size=None):
        """Run the crawler to fetch and process all events."""
        cls._initialize()
        end_block = cls._w3.eth.block_number
        cls._last_block = end_block

        if chunk_size is None:
            chunk_size = cls.DEFAULT_CHUNK_SIZE

        if start_block is None:
            start_block = cls.START_BLOCK

        if cls._last_block <= start_block:
            return

        logger.info(
            f"Crawling blocks from {start_block} to {end_block} (latest) with maximum of {num_workers} workers"
        )

        num_chunks = (end_block - start_block) // chunk_size + 1
        chunks = [
            (
                start_block + i * chunk_size,
                min(start_block + (i + 1) * chunk_size - 1, end_block),
            )
            for i in range(num_chunks)
        ]

        all_deposits = list()
        all_withdrawals = list()

        if num_workers > 1:
            logger.info(f"Processing {len(chunks)} chunks with maximum of {num_workers} workers...")
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_workers
            ) as executor:
                future_to_chunk = {
                    executor.submit(cls._process_chunk, chunk): chunk
                    for chunk in chunks
                }

                for future in concurrent.futures.as_completed(future_to_chunk):
                    chunk = future_to_chunk[future]
                    result = future.result()
                    if result:
                        all_deposits.extend(result["deposits"])
                        all_withdrawals.extend(result["withdrawals"])
                        logger.info(f"Completed chunk {chunk[0]}-{chunk[1]}")
        else:
            for chunk in chunks:
                result = cls._process_chunk(chunk)
                if result:
                    all_deposits.extend(result["deposits"])
                    all_withdrawals.extend(result["withdrawals"])

        logger.info(
            f"Found {len(all_deposits)} deposits and {len(all_withdrawals)} withdrawals in total"
        )

        cls._deposit_balances = cls._process_events(all_deposits, is_withdrawal=False)
        cls._withdrawal_balances = cls._process_events(
            all_withdrawals, is_withdrawal=True
        )
        cls._final_balances = cls._calculate_final_balances()

        return cls._final_balances

    @classmethod
    def get_tvl_in_usdc(cls, start_block=None, num_workers=10, chunk_size=None):
        """Get the total value locked (TVL) in USDC equivalent."""
        if start_block is None:
            start_block = cls.START_BLOCK

        cls._run_crawler(
            start_block=start_block, num_workers=num_workers, chunk_size=chunk_size
        )

        return sum(
            MarketPriceUtility.convert_token_to_usdc(token_name=token, amount=amount)
            for token, amount in cls._final_balances.items()
        )

    @classmethod
    def get_token_balances(cls, start_block=None, num_workers=10, chunk_size=None):
        """Get the token balances."""
        if start_block is None:
            start_block = cls.START_BLOCK

        cls._run_crawler(
            start_block=start_block, num_workers=num_workers, chunk_size=chunk_size
        )

        return cls._final_balances.copy()
