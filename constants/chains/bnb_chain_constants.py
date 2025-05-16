import os

from constants.chains.chain_base import ChainConstantsBaseClass


class BNBChainConstants(ChainConstantsBaseClass):

    CHAIN_NAME = "BNB"

    PUBLIC_CONTRACT_ADDRESS = "0xd0ec30e908D16f581417C54be3c6Ff3189AbD259"

    CHAIN_ID = 56

    TOKEN_INFO = {
        "USDC": {
            "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "decimal": 18,
        },
        "USDT": {
            "address": "0x55d398326f99059fF775485246999027B3197955",
            "decimal": 18,
        },
        "BTC": {"address": "0x0555E30da8f98308EdB960aa94C0Db47230d2B9c", "decimal": 8},
    }

    ABI_STRING = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BridgedDeposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"string","name":"withdrawalId","type":"string"}],"name":"BridgedWithdrawal","type":"event"}]'

    HTTP_PROVIDER = os.getenv("BNB_HTTP_PROVIDER", "https://bsc-dataseed-public.bnbchain.org/")

    CHUNK_SIZE = 10000

    MIN_START_BLOCK = 45973240

class CollateralDataBNBChainConstants(BNBChainConstants):

    ABI_STRING = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"submitter","type":"address"},{"indexed":false,"internalType":"uint256","name":"collateralRatio","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"info","type":"string"}],"name":"CollateralDataPushed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"bool","name":"isWhitelisted","type":"bool"}],"name":"WhitelistUpdated","type":"event"},{"inputs":[],"name":"getCollateralRatioDecimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_collateralRatio","type":"uint256"},{"internalType":"string","name":"_info","type":"string"}],"name":"pushCollateralData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"bool","name":"_status","type":"bool"}],"name":"updateWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'

    PUBLIC_CONTRACT_ADDRESS = "0xAeF2639c1Bd8392712749C6e92CDFDB747e3827D"

    EVENT_NAME = "CollateralDataPushed"

    PAST_EVENT_LOOKUP_BLOCK_RANGE = 50000

    CHUNK_SIZE = 5000

