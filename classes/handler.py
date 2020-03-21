from abc import ABC, abstractmethod
from telegram import Update
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

    def fallback(self, update: Update, context: CallbackContext):
        update.message.reply_text('Command wasn\'t found or something went wrong')

class HandlerHelpers():
    @staticmethod
    def get_teams(chat_id: int) -> list:
        return list(map(lambda x: x['name'], App.db.get_teams().find({
            'chat_id': chat_id,
        }, {'_id': 0, 'name': 1})))

    @staticmethod
    def make_teams_regex(chat_id):
        return '|'.join(HandlerHelpers.get_teams(chat_id))

    @staticmethod
    def get_team_members(chat_id, team) -> list:
        return App.db.get_teams().find_one({
            'name': team,
            'chat_id': chat_id,
        }, {'_id': 0, 'members': 1})['members']

    @staticmethod
    def check_teams_existence(update: Update) -> bool:
        res = len(HandlerHelpers.get_teams(update.message.chat_id)) > 0

        if not res:
            update.message.reply_text(
                'Before using MentionerBot, make sure at least one team was added, try /addteam'
            )

        return res
