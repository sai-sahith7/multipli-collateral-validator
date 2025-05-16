from strategies.base_strategy import BaseStrategy
from utilities.multipli_api_utility import MultipliAPIUtil


class APIStrategy(BaseStrategy):
    """Strategy to compare API TVL with Binance TVL."""

    @classmethod
    def execute(cls):
        multipli_api_tvl_in_usdc = MultipliAPIUtil.get_total_tvl_in_usdc()
        binance_tvl_in_usdc = cls.get_tvl_from_binance()

        percentage_match = (binance_tvl_in_usdc / multipli_api_tvl_in_usdc) * 100
        percentage_match = round(percentage_match, 2)

        return float(percentage_match)
