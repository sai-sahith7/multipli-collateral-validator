class CoinGeckoConstants:

    API_V3_BASE_URL = "https://api.coingecko.com/api/v3"
    MARKET_PRICE_ENDPOINT = "/simple/price"

    TOKEN_NAME_TO_IDS = {
        "USDC": "usd",
        "USDT": "tether",
        "BTC": "bitcoin",
    }

    @classmethod
    def get_token_id_from_token_name(cls, token_name):
        return cls.TOKEN_NAME_TO_IDS.get(token_name.upper(), None)
