import logging

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        extra = "allow"
        env_file = ".env"

logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)