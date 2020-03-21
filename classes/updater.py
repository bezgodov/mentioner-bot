from telegram.ext import Updater as _Updater

from classes.helpers import full_root_path
from classes.config import get_token, get_proxy

class Updater():
    def __init__(self):
        request_kwargs = {'proxy_url': get_proxy()}

        self.updater = _Updater(
            token=get_token(),
            use_context=True,
            request_kwargs=request_kwargs if get_proxy() else None
        )

    def run_updater(self):
        self.updater.start_polling()
        self.updater.idle()

    def get_updater(self) -> _Updater:
        return self.updater
