from telegram.ext import Updater as _Updater, PicklePersistence
from classes.helpers import full_root_path
from classes.config import get_token, get_proxy

class Updater():
    request_kwargs = {'proxy_url': get_proxy()}

    def __init__(self):
        persistence = PicklePersistence(
            filename=full_root_path('assets/data/chat_data'),
            store_chat_data=True,
            store_bot_data=False,
            store_user_data=False,
        )

        self.updater = _Updater(
            token=get_token(),
            use_context=True,
            persistence=persistence,
            request_kwargs=Updater.request_kwargs if get_proxy() else None
        )

    def run_updater(self):
        self.updater.start_polling()
        self.updater.idle()

    def get_updater(self):
        return self.updater
