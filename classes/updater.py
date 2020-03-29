import sys
import logging
from telegram.ext import Updater as _Updater

from classes.helpers import full_root_path
from classes.config import get_token, get_proxy, get_platform, get_heroku_config

class Updater():
    def __init__(self):
        request_kwargs = {'proxy_url': get_proxy()}

        self.updater = _Updater(
            token=get_token(),
            use_context=True,
            request_kwargs=request_kwargs if get_proxy() else None
        )

    def run_updater(self):
        if get_platform() == 'Heroku':
            port = get_heroku_config()['HEROKU_PORT']
            app_name = get_heroku_config()['HEROKU_APP_NAME']

            if not app_name or not port:
                logging.error("No app name or port were specified, add it to .env")
                sys.exit(1)

            # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=get_token()
            )

            self.updater.bot.set_webhook(f'https://{app_name}.herokuapp.com/{get_token()}')
        else:
            self.updater.start_polling()

        self.updater.idle()

    def get_updater(self) -> _Updater:
        return self.updater
