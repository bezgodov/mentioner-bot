import os
from typing import Union

def is_debug() -> Union[str, bool]:
    return os.getenv('BOT_DEBUG', False)

def get_token() -> str:
    token = os.getenv('BOT_TOKEN', None)
    if token is None:
        raise ValueError('Bot token wasn\'t set')
    return token

def get_proxy() -> str:
    return os.getenv('PROXY_URL', None)

def get_config() -> dict:
    return {
        'BOT_DEBUG': is_debug(),
        'BOT_TOKEN': get_token(),
        'PROXY_URL': get_proxy(),

        'MONGO_USERNAME': os.getenv('MONGO_USERNAME', 'root'),
        'MONGO_PASSWORD': os.getenv('MONGO_PASSWORD', 'pass'),
        'MONGO_HOST': os.getenv('MONGO_HOST', 'mongo'),
        'MONGO_PORT': os.getenv('MONGO_PORT', '27017'),
        'MONGO_DB_NAME': os.getenv('MONGO_DB_NAME', 'chat_mentioner'),
        'MONGO_COLLECTION_NAME': os.getenv('MONGO_COLLECTION_NAME', 'teams'),
    }
