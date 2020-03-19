from telegram.ext import CommandHandler, CallbackContext

from classes.handler import BaseHandler

class GetTeams(BaseHandler):
    GETTING_END = range(-1, 0)

    def init(self):
        self.updater.dispatcher.add_handler(CommandHandler(self.name, self.get))

    def get(self, update, context: CallbackContext):
        _teams = ", ".join(self.get_teams())
        update.message.reply_text(_teams)

        return GetTeams.GETTING_END
