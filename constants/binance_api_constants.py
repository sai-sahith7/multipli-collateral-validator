import os


class BinanceAPICredentials:
    API_KEY = None
    API_SECRET = None

    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret


class BinanceAPIMarketConfig:
    MARKET_PAIR = None
    RECIPROCAL = False

    def __init__(self, market_pair, reciprocal=False):
        self.MARKET_PAIR = market_pair
        self.RECIPROCAL = reciprocal


class BinanceAPIConstants:
    API_BASE_URL = "https://api.binance.com"

    MARKET_PRICE_ENDPOINT = "/api/v3/ticker/price"
    SYMBOL_MAP = {
        "USDT": BinanceAPIMarketConfig(market_pair="USDCUSDT", reciprocal=True),
        "BTC": BinanceAPIMarketConfig(market_pair="BTCUSDC"),
    }

    WALLET_ENDPOINT = "/sapi/v1/asset/wallet/balance"
    RECV_WINDOW = 5000
    ACCOUNTS = [
        BinanceAPICredentials(
            api_key=os.getenv("BINANCE_ACCOUNT_1_API_KEY"),
            api_secret=os.getenv("BINANCE_ACCOUNT_1_API_SECRET"),
        ),
        BinanceAPICredentials(
            api_key=os.getenv("BINANCE_ACCOUNT_2_API_KEY"),
            api_secret=os.getenv("BINANCE_ACCOUNT_2_API_SECRET"),
        ),
        BinanceAPICredentials(
            api_key=os.getenv("BINANCE_ACCOUNT_3_API_KEY"),
            api_secret=os.getenv("BINANCE_ACCOUNT_3_API_SECRET"),
        ),
        BinanceAPICredentials(
            api_key=os.getenv("BINANCE_ACCOUNT_4_API_KEY"),
            api_secret=os.getenv("BINANCE_ACCOUNT_4_API_SECRET"),
        ),
    ]

    @classmethod
    def get_market_pair_from_token(cls, token) -> BinanceAPIMarketConfig:
        return cls.SYMBOL_MAP.get(token.upper(), None)
