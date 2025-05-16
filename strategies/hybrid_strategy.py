from decimal import Decimal

from strategies.base_strategy import BaseStrategy
from strategies.crawler_strategy import CrawlerStrategy
from utilities.multipli_api_utility import MultipliAPIUtil


class HybridStrategy(BaseStrategy):
    """Strategy to take max of API & Crawler TVL, compare with Binance TVL."""

    @classmethod
    def execute(cls):
        """Take the max of both TVLs, compare with Binance TVL, and return percentage."""
        multipli_api_tvl_in_usdc = MultipliAPIUtil.get_total_tvl_in_usdc()
        tvl_from_chain_in_usdc = CrawlerStrategy.get_total_tvl_in_usdc()

        hybrid_tvl_for_calculation = max(multipli_api_tvl_in_usdc, tvl_from_chain_in_usdc)

        tvl_from_binance_in_usdc = Decimal(cls.get_tvl_from_binance())

        percentage_match = (tvl_from_binance_in_usdc / hybrid_tvl_for_calculation) * 100
        percentage_match = round(percentage_match, 2)

        return float(percentage_match)
