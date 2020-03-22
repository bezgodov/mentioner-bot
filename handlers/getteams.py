from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from classes.handler import BaseHandler, HandlerHelpers
from classes.filters import filters

class GetTeams(BaseHandler):
    GETTING_END = range(-1, 0)

    def init(self):
        self.updater.dispatcher.add_handler(CommandHandler(self.name, self.get))

    def get(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        teams = HandlerHelpers.get_teams(chat_id)

        if len(teams) > 0:
            update.message.reply_text(', '.join(teams))
        else:
            update.message.reply_text('No teams were found')

        return GetTeams.GETTING_END
