from abc import ABC, abstractmethod
from telegram.ext import DictPersistence, Dispatcher, CallbackContext

from classes.app import App

class BaseHandler(ABC):
    def __init__(self, name):
        self.name = name
        self.updater = App.updater.get_updater()
        self.chat_data: dict = self.updater.dispatcher.chat_data
        self.init()

    @abstractmethod
    def init(self):
        pass

    def get_chat_data_teams(self) -> dict:
        if not self.chat_data.get('teams'):
            self.chat_data['teams'] = {}

        return self.chat_data.get('teams', {})

    def get_teams(self):
        return list(self.get_chat_data_teams().keys())

    def make_teams_regex(self):
        return '|'.join(self.get_teams())

    def get_team_members(self, team):
        return list(self.get_chat_data_teams().get(team, {}).get('members', {}))

    def fallback(self, update, context: CallbackContext):
        update.message.reply_text('Command was\'t found or something went wrong')
