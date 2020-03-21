import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler
from classes.app import App

class RemoveTeam(BaseHandler):
    CHOOSING_END, CHOOSING_TEAM = range(-1, 1)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start, filters=App.filters.admin),
            ],
            states={
                RemoveTeam.CHOOSING_TEAM: [MessageHandler(Filters.text, self.choose_team)],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)]
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update, context: CallbackContext):
        markup = ReplyKeyboardMarkup(map(lambda x: [x], self.get_teams()), one_time_keyboard=True)
        update.message.reply_text(
            'Choose team to remove',
            reply_markup=markup
        )

        return RemoveTeam.CHOOSING_TEAM

    def choose_team(self, update, context: CallbackContext):
        team = update.message.text

        if not re.match(f'^({self.make_teams_regex()})$', team):
            update.message.reply_text(f'Team "{team}" was\'t found, try again')
            return RemoveTeam.CHOOSING_TEAM

        self.get_chat_data_teams().pop(team, None)
        update.message.reply_text(
            f'Team "{team}" was successfully removed',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        return RemoveTeam.CHOOSING_END
