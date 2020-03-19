import os
from typing import Union

def is_debug() -> Union[str, bool]:
    return os.getenv('BOT_DEBUG', False)

def get_token() -> str:
    token = os.getenv('BOT_TOKEN', None)
    if token is None:
        raise ValueError('Bot token was\'t set')
    return token

def get_proxy() -> str:
    return os.getenv('PROXY_URL', None)
