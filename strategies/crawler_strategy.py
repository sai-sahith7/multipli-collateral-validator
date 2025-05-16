from decimal import Decimal

from strategies.base_strategy import BaseStrategy
from utilities.crawlers.bnb_crawler_utility import BNBChainCrawler
from utilities.crawlers.ethereum_crawler_utility import EthereumChainCrawler


class CrawlerStrategy(BaseStrategy):
    """
    Strategy to compare Crawler TVL with Binance TVL.

    Note: This strategy is only available for public contracts. If you are an institutional user,
    Kindly use API Strategy instead. For further information, contact us at support@multipli.fi
    """

    bnb_utility_class = BNBChainCrawler
    ethereum_utility_class = EthereumChainCrawler

    @classmethod
    def execute(cls):
        tvl_from_chain_in_usdc = cls.get_total_tvl_in_usdc()
        tvl_from_binance_in_usdc = Decimal(cls.get_tvl_from_binance())

        percentage_match = (tvl_from_binance_in_usdc / tvl_from_chain_in_usdc) * 100
        percentage_match = round(percentage_match, 2)

        return float(percentage_match)

    @classmethod
    def get_total_tvl_in_usdc(cls):
        bnb_chain_tvl_in_usdc = cls._get_tvl_in_usdc(
            utiltiy_class=cls.bnb_utility_class,
        )
        eth_chain_tvl_in_usdc = cls._get_tvl_in_usdc(
            utiltiy_class=cls.ethereum_utility_class,
        )

        tvl_from_chain_in_usdc = Decimal(bnb_chain_tvl_in_usdc) + Decimal(
            eth_chain_tvl_in_usdc
        )

        # Private funds that were deposited through the public contract but withdrawn via a different contract.
        PRIVATE_FUND_WITHDRAWAL_ADJUSTMENT = Decimal("-15000000.00")
        # v1 contract deposits which are to be adjusted after shift to v2
        V1_CONTRACT_DEPOSIT_ADJUSTMENT = Decimal("4819162.5300")

        TOTAL_ADJUSTMENT = PRIVATE_FUND_WITHDRAWAL_ADJUSTMENT + V1_CONTRACT_DEPOSIT_ADJUSTMENT

        tvl_from_chain_in_usdc = tvl_from_chain_in_usdc + TOTAL_ADJUSTMENT

        return tvl_from_chain_in_usdc

    @staticmethod
    def _get_tvl_in_usdc(utiltiy_class):
        # This is set to None, to use the default start_block value assigned to the crawler
        start_block = None
        return utiltiy_class.get_tvl_in_usdc(start_block=start_block)
