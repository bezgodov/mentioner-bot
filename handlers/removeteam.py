import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
from classes.app import App
from classes.queue import Queue
from classes.filters import filters

class RemoveTeam(BaseHandler):
    CHOOSING_END, CHOOSING_TEAM = range(-1, 1)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start, filters=filters.admin),
            ],
            states={
                RemoveTeam.CHOOSING_TEAM: [
                    CommandHandler('cancel', self.cancel),
                    MessageHandler(Filters.text & ~filters.cancel, self.choose_team)
                ],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)],
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update: Update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)

        chat_id = update.message.chat.id

        if not HandlerHelpers.check_teams_existence(update):
            return RemoveTeam.CHOOSING_END

        markup = ReplyKeyboardMarkup(map(lambda x: [x], HandlerHelpers.get_teams(chat_id)), one_time_keyboard=True)
        message = update.message.reply_text(
            'Choose team to remove',
            reply_markup=markup
        )

        Queue.add(message.chat.id, message.message_id)

        return RemoveTeam.CHOOSING_TEAM

    def choose_team(self, update: Update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)
        
        chat_id = update.message.chat.id
        team = update.message.text

        if not re.match(f'^({HandlerHelpers.make_teams_regex(chat_id)})$', team):
            message = update.message.reply_text(f'Team "{team}" wasn\'t found, try again')
            Queue.add(message.chat.id, message.message_id)
            return RemoveTeam.CHOOSING_TEAM

        document = App.db.get_teams().find_one_and_delete({
            'chat_id': chat_id,
            'name': team,
        })
        if document:
            message = update.message.reply_text(
                f'Team "{team}" was successfully removed',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
            )
            Queue.add(message.chat.id, message.message_id)
        else:
            message = update.message.reply_text(
                f'Team "{team}" wasn\'t removed due to some errors, try again later',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
            )
            Queue.add(message.chat.id, message.message_id)

        Queue.clean(update.message.chat.id, timeout=30)
        return RemoveTeam.CHOOSING_END
