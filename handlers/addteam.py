from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler

class AddTeam(BaseHandler):
    CHOOSING_END, CHOOSING_NAME = range(-1, 1)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start),
            ],
            states={
                AddTeam.CHOOSING_NAME: [MessageHandler(Filters.text, self.choose_name)],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)]
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update, context: CallbackContext):
        update.message.reply_text('Choose a team name')

        return AddTeam.CHOOSING_NAME

    def choose_name(self, update, context: CallbackContext):
        name = update.message.text

        # TODO: add regex
        if len(name) > 1 and len(name) < 16 and not name.startswith('@') and not name.startswith('/'):
            if name.lower() in list(map(str.lower, self.get_chat_data_teams().keys())):
                update.message.reply_text(
                    f'Team "{name}" already exists, try another name'
                )
                return AddTeam.CHOOSING_NAME
            else:
                self.get_chat_data_teams()[name] = {}
                update.message.reply_text(
                    f'Team "{name}" was successfully created'
                )
        else:
            update.message.reply_text(
                f'Team "{name}" was\'t created cause name contains incorrect symbols, try again'
            )
            return AddTeam.CHOOSING_NAME

        return AddTeam.CHOOSING_END
