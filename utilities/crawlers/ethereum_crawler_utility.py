from constants.chains.ethereum_chain_constants import EthereumChainConstants
from utilities.crawlers.chain_crawler_base_utility import BlockchainCrawlerBase


class EthereumChainCrawler(BlockchainCrawlerBase):
    """A class to crawl the Ethereum blockchain for deposit and withdrawal events."""

    # Override class constants
    CHAIN_NAME = EthereumChainConstants.CHAIN_NAME
    START_BLOCK = EthereumChainConstants.MIN_START_BLOCK
    DEFAULT_CHUNK_SIZE = EthereumChainConstants.CHUNK_SIZE

    # Initialize Web3 and contract
    http_provider_url = EthereumChainConstants.get_http_provider()
    contract_address = EthereumChainConstants.get_public_contract_address()
    abi_json = EthereumChainConstants.get_abi_json()

    _token_info = EthereumChainConstants.get_token_info()
