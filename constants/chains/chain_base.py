import json


class ChainConstantsBaseClass:

    PUBLIC_CONTRACT_ADDRESS = None
    TOKEN_INFO = None
    ABI_STRING = None
    HTTP_PROVIDER = None
    CHAIN_ID = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_public_contract_address(cls):
        return cls.PUBLIC_CONTRACT_ADDRESS

    @classmethod
    def get_token_info(cls):
        return cls.TOKEN_INFO

    @classmethod
    def get_abi_string(cls):
        return cls.ABI_STRING

    @classmethod
    def get_abi_json(cls):
        return json.loads(cls.get_abi_string())

    @classmethod
    def get_http_provider(cls):
        return cls.HTTP_PROVIDER

    @classmethod
    def get_chain_id(cls):
        return cls.CHAIN_ID

    @classmethod
    def get_decimal_by_token(cls, token):
        token_info = cls.get_token_info().get(token, None)
        if token_info is None:
            return None
        return int(token_info.get("decimal", None))

    @classmethod
    def get_token_contract(cls, token):
        token_info = cls.get_token_info().get(token, None)
        if token_info is None:
            return None
        return token_info.get("contract", None)
