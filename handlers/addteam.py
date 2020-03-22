import re

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
from classes.app import App
from classes.filters import filters

class AddTeam(BaseHandler):
    CHOOSING_END, CHOOSING_NAME = range(-1, 1)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start, filters=filters.admin & filters.defined_command),
            ],
            states={
                AddTeam.CHOOSING_NAME: [
                    CommandHandler('cancel', self.cancel),
                    MessageHandler(Filters.text, self.choose_name),
                ],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)],
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update, context: CallbackContext):
        update.message.reply_text('Choose a team name')

        return AddTeam.CHOOSING_NAME

    def choose_name(self, update: Update, context: CallbackContext):
        name = update.message.text

        if re.match(r'^[0-9a-zа-яё._-]{2,16}$', name.lower(), re.IGNORECASE):
            if App.db.get_teams().find_one({
                'name': re.compile(f'^{name.lower()}$', re.IGNORECASE),
                'chat_id': update.message.chat_id
            }):
                update.message.reply_text(
                    f'Team "{name}" already exists, try another name'
                )
                return AddTeam.CHOOSING_NAME
            else:
                App.db.get_teams().insert_one({
                    'name': name,
                    'chat_id': update.message.chat_id,
                    'members': [],
                })
                update.message.reply_text(
                    f'Team "{name}" was successfully created'
                )
        else:
            update.message.reply_text(
                f'Team "{name}" wasn\'t created cause name contains incorrect symbols, try again'
            )
            return AddTeam.CHOOSING_NAME

        return AddTeam.CHOOSING_END
