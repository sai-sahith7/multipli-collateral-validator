import time
from decimal import Decimal

import ccxt

from constants.binance_api_constants import BinanceAPIConstants


class BinanceAPIUtil:
    """Utility for fetching TVL data from Binance."""

    @staticmethod
    def _make_api_request(credentials):
        binance = ccxt.binance({
            'apiKey': credentials.API_KEY,
            'secret': credentials.API_SECRET,
        })

        params = {
            'timestamp': int(time.time() * 1000),
            'quoteAsset': 'USDC',
            'recvWindow': 5000,
        }

        balance = binance.sapi_get_asset_wallet_balance(params)
        return balance

    @staticmethod
    def _calculate_total_usdc_balance(wallet_data):
        """Calculate total USDC balance from wallet data."""
        if not wallet_data:
            return Decimal("0")

        total_balance = Decimal("0")
        for wallet in wallet_data:
            if wallet.get("activate", False):
                try:
                    balance = Decimal(wallet.get("balance", "0"))
                    total_balance += balance
                except (ValueError, TypeError):
                    continue

        return total_balance

    @classmethod
    def fetch_tvl_in_usdc(cls):
        """
        Fetch TVL data from all Binance accounts in USDC.

        Returns:
            Decimal: Total Value Locked (TVL) in USDC
        """
        total_usdc = Decimal("0")

        for account in BinanceAPIConstants.ACCOUNTS:
            wallet_data = cls._make_api_request(account)
            account_usdc = cls._calculate_total_usdc_balance(wallet_data)
            total_usdc += account_usdc

        return total_usdc