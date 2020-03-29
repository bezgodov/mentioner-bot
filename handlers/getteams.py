from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from classes.handler import BaseHandler, HandlerHelpers
from classes.queue import Queue
from classes.filters import filters

class GetTeams(BaseHandler):
    GETTING_END = range(-1, 0)

    def init(self):
        self.updater.dispatcher.add_handler(CommandHandler(self.name, self.get))

    def get(self, update: Update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)

        chat_id = update.message.chat.id
        teams = HandlerHelpers.get_teams(chat_id)

        if len(teams) > 0:
            message = update.message.reply_text(', '.join(teams))
            Queue.add(message.chat.id, message.message_id, timeout=300)
        else:
            message = update.message.reply_text('No teams were found')
            Queue.add(message.chat.id, message.message_id)

        Queue.clean(update.message.chat.id)
        return GetTeams.GETTING_END
