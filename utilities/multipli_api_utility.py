from decimal import Decimal

import requests

from constants.multipli_api_constants import MultipliAPIConstants


class MultipliAPIUtil:
    """Utility for interacting with Multipli API."""

    BASE_URL = MultipliAPIConstants.BASE_URL
    PUBLIC_CONTRACT_ENDPOINT = MultipliAPIConstants.PUBLIC_CONTRACT_ENDPOINT
    PRIVATE_CONTRACT_ENDPOINT = MultipliAPIConstants.PRIVATE_CONTRACT_ENDPOINT
    API_KEY = MultipliAPIConstants.MULTIPLI_API_KEY

    HEADERS = {"MULTIPLI-API-KEY": API_KEY}

    @classmethod
    def get_total_tvl_in_usdc(cls):
        """Fetch total TVL from the Multipli API."""
        public_tvl = cls.get_public_contract_tvl_in_usdc()
        private_tvl = cls.get_private_contract_tvl_in_usdc()
        return public_tvl + private_tvl

    @classmethod
    def get_public_contract_tvl_in_usdc(cls):
        """Fetch TVL for public contracts in USDC."""
        try:
            response = requests.get(
                f"{cls.BASE_URL}{cls.PUBLIC_CONTRACT_ENDPOINT}",
                headers=cls.HEADERS,
            )
            if response.status_code == 401:
                raise Exception("Unauthorized: Invalid API key for public contract TVL.")
            if response.status_code == 403:
                return Decimal("0.0")
            response.raise_for_status()
            data = response.json()
            return Decimal(data.get("payload", {}).get("tvl_in_usdc", 0))
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch public contract TVL: {e}")

    # This method is only for institutional users, 
    # if you are a public validator, you wouldn't be able to access this endpoint, 
    # if you are an institutional user, your API key also acts as an identifier
    #   for your institution 
    # contract information as well)
    @classmethod
    def get_private_contract_tvl_in_usdc(cls):
        """Fetch TVL for private contracts in USDC."""
        try:
            response = requests.get(
                f"{cls.BASE_URL}{cls.PRIVATE_CONTRACT_ENDPOINT}",
                headers=cls.HEADERS,
            )
            if response.status_code == 401:
                raise Exception("Unauthorized: Invalid API key for private contract TVL.")
            if response.status_code == 403:
                return Decimal("0.0")
            response.raise_for_status()
            data = response.json()
            return Decimal(data.get("payload", {}).get("tvl_in_usdc", 0))
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch private contract TVL: {e}")
