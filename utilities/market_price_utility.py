from decimal import Decimal

from constants.binance_api_constants import BinanceAPIConstants
from constants.coingecko_constants import CoinGeckoConstants
import requests


class MarketPriceUtility:

    COINGECKO_BASE_URL = CoinGeckoConstants.API_V3_BASE_URL
    COINGECKO_ENDPOINT = CoinGeckoConstants.MARKET_PRICE_ENDPOINT

    BINANCE_MARKET_BASE_URL = BinanceAPIConstants.API_BASE_URL
    BINANCE_ENDPOINT = BinanceAPIConstants.MARKET_PRICE_ENDPOINT

    @classmethod
    def get_token_price_in_usdc(cls, token_name):
        try:
            token_id = CoinGeckoConstants.get_token_id_from_token_name(token_name)
            response = requests.get(
                f"{cls.COINGECKO_BASE_URL}{cls.COINGECKO_ENDPOINT}",
                params={"ids": token_id, "vs_currencies": "usd"},
            )
            response.raise_for_status()
            data = response.json()
            return data.get(token_id, {}).get("usd")
        except requests.RequestException as error:
            # Fallback to Binance Market API

            market_pair_obj = BinanceAPIConstants.get_market_pair_from_token(
                token=token_name
            )
            response = requests.get(
                f"{cls.BINANCE_MARKET_BASE_URL}{cls.BINANCE_ENDPOINT}",
                params={
                    "symbol": market_pair_obj.MARKET_PAIR,
                },
            )
            response.raise_for_status()
            data = response.json()
            price = Decimal(data.get("price"))
            if market_pair_obj.RECIPROCAL:
                return Decimal(1 / price)
            else:
                return price

    @classmethod
    def convert_token_to_usdc(cls, token_name, amount):
        token_name = token_name.upper()
        if token_name == "USDC":
            return amount
        price = cls.get_token_price_in_usdc(token_name=token_name)
        if price is None:
            raise ValueError("Failed to fetch token price.")
        return Decimal(amount) * Decimal(price)
