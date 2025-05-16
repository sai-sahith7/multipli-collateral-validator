import os

class MultipliAPIConstants:
    BASE_URL = "https://api.multipli.fi/multipli/v1/"

    PUBLIC_CONTRACT_ENDPOINT = "public-contract-tvl/"
    PRIVATE_CONTRACT_ENDPOINT = "private-contract-tvl/"

    MULTIPLI_API_KEY = os.getenv("MULTIPLI_API_KEY")
