import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
from classes.queue import Queue
from classes.filters import filters

class Mention(BaseHandler):
    CHOOSING_END, MENTION = range(-1, 1)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start),
            ],
            states={
                Mention.MENTION: [
                    CommandHandler('cancel', self.cancel),
                    MessageHandler(Filters.text & ~filters.cancel, self.mention),
                ],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)],
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id

        Queue.add(update.message.chat.id, update.message.message_id)

        if not HandlerHelpers.check_teams_existence(update):
            return Mention.CHOOSING_END

        markup = ReplyKeyboardMarkup(map(lambda x: [x], HandlerHelpers.get_teams(chat_id)), one_time_keyboard=True)
        message = update.message.reply_text(
            f'Choose a team',
            reply_markup=markup
        )

        Queue.add(message.chat.id, message.message_id)

        return Mention.MENTION

    def mention(self, update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)

        chat_id = update.message.chat.id
        team = update.message.text

        if not re.match(f'^({HandlerHelpers.make_teams_regex(chat_id)})$', team):
            message = update.message.reply_text(f'Team "{team}" wasn\'t found, try again')
            Queue.add(message.chat.id, message.message_id)
            return Mention.MENTION

        members = HandlerHelpers.get_team_members(chat_id, team)

        if members:
            update.message.reply_text(
                ' '.join(members),
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
            )
        else:
            message = update.message.reply_text(
                'Members weren\'t found or something went wrong',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
            )
            Queue.add(message.chat.id, message.message_id)

        Queue.clean(update.message.chat.id, timeout=30)
        return Mention.CHOOSING_END
