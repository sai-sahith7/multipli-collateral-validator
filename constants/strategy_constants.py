import enum
import os

from constants.chains.avalanche_chain_constants import AvalancheChainConstants
from constants.chains.bnb_chain_constants import CollateralDataBNBChainConstants
from strategies.api_strategy import APIStrategy
from strategies.crawler_strategy import CrawlerStrategy
from strategies.hybrid_strategy import HybridStrategy


class StrategyConstants:

    class STRATEGY_CHOICES(enum.Enum):
        CRAWLER_STRATEGY = "CRAWLER"
        API_STRATEGY = "API"
        HYBRID_STRATEGY = "HYBRID"


    STRATEGY_MAPPING = {
        STRATEGY_CHOICES.CRAWLER_STRATEGY.value: CrawlerStrategy,
        STRATEGY_CHOICES.API_STRATEGY.value: APIStrategy,
        STRATEGY_CHOICES.HYBRID_STRATEGY.value: HybridStrategy,
    }

    @classmethod
    def get_strategy_class(cls):
        picked_strategy = os.getenv("STRATEGY")
        return cls.STRATEGY_MAPPING.get(picked_strategy, None)

    @classmethod
    def get_strategy_name(cls):
        picked_strategy = os.getenv("STRATEGY")
        return picked_strategy

    @staticmethod
    def get_data_push_enabled_chain_constants_classes():
        chain_classes = list()
        is_bsc_enabled = bool(int(os.getenv("ENABLE_BSC_TO_PUSH_DATA", True)))
        is_avalanche_enabled = bool(int(os.getenv("ENABLE_AVALANCHE_TO_PUSH_DATA", True)))
        if is_bsc_enabled:
            chain_classes.append(CollateralDataBNBChainConstants)
        if is_avalanche_enabled:
            chain_classes.append(AvalancheChainConstants)
        if len(chain_classes) == 0:
            return None
        else:
            return chain_classes