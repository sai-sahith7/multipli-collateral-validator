import os

from constants.chains.chain_base import ChainConstantsBaseClass


class AvalancheChainConstants(ChainConstantsBaseClass):

    CHAIN_NAME = "AVALANCHE"

    PUBLIC_CONTRACT_ADDRESS = "0x95F36E1e2F9E62986A52805fed810506FE887f9A"

    CHAIN_ID = 43114

    ABI_STRING = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"submitter","type":"address"},{"indexed":false,"internalType":"uint256","name":"collateralRatio","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"info","type":"string"}],"name":"CollateralDataPushed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"bool","name":"isWhitelisted","type":"bool"}],"name":"WhitelistUpdated","type":"event"},{"inputs":[],"name":"getCollateralRatioDecimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_collateralRatio","type":"uint256"},{"internalType":"string","name":"_info","type":"string"}],"name":"pushCollateralData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"bool","name":"_status","type":"bool"}],"name":"updateWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'

    HTTP_PROVIDER = os.getenv("AVALANCHE_HTTP_PROVIDER", "https://avalanche-c-chain-rpc.publicnode.com")

    EVENT_NAME = "CollateralDataPushed"

    PAST_EVENT_LOOKUP_BLOCK_RANGE = 50000

    CHUNK_SIZE = 40000
