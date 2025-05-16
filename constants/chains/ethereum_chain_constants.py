import os

from constants.chains.chain_base import ChainConstantsBaseClass


class EthereumChainConstants(ChainConstantsBaseClass):

    CHAIN_NAME = "ETHEREUM"

    PUBLIC_CONTRACT_ADDRESS = "0x5D39456B62d6645DE8fb4556c05a9FF97c10de81"

    CHAIN_ID = 1

    TOKEN_INFO = {
        "USDC": {
            "decimal": 6,
            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eb48",
        },
        "USDT": {
            "decimal": 6,
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        },
        "BTC": {
            "decimal": 8,
            "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        },
    }

    ABI_STRING = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BridgedDeposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"string","name":"withdrawalId","type":"string"}],"name":"BridgedWithdrawal","type":"event"}]'

    HTTP_PROVIDER = os.getenv("ETHEREUM_HTTP_PROVIDER", "https://ethereum-rpc.publicnode.com")

    MIN_START_BLOCK = 21633270

    CHUNK_SIZE = 40000

