from web3 import Web3

from constants.chains.bnb_chain_constants import BNBChainConstants
from utilities.crawlers.chain_crawler_base_utility import BlockchainCrawlerBase


class BNBChainCrawler(BlockchainCrawlerBase):
    """A class to crawl the BNB blockchain for deposit and withdrawal events."""

    CHAIN_NAME = BNBChainConstants.CHAIN_NAME
    START_BLOCK = BNBChainConstants.MIN_START_BLOCK
    DEFAULT_CHUNK_SIZE = BNBChainConstants.CHUNK_SIZE

    http_provider_url = BNBChainConstants.HTTP_PROVIDER
    contract_address = Web3.to_checksum_address(
        BNBChainConstants.PUBLIC_CONTRACT_ADDRESS
    )
    abi_json = BNBChainConstants.ABI_STRING

    _token_info = BNBChainConstants.get_token_info()
