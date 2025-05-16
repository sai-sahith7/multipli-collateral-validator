from utilities.binance_api_utility import BinanceAPIUtil


class BaseStrategy:
    """Base class for TVL calculation strategies."""

    @staticmethod
    def get_tvl_from_binance():
        tvl_in_usdc = BinanceAPIUtil.fetch_tvl_in_usdc()
        return tvl_in_usdc
