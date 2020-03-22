import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
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
        chat_id = update.message.chat_id

        if not HandlerHelpers.check_teams_existence(update):
            return Mention.CHOOSING_END

        markup = ReplyKeyboardMarkup(map(lambda x: [x], HandlerHelpers.get_teams(chat_id)), one_time_keyboard=True)
        update.message.reply_text(
            f'Choose a team',
            reply_markup=markup
        )

        return Mention.MENTION

    def mention(self, update, context: CallbackContext):
        chat_id = update.message.chat_id
        team = update.message.text

        if not re.match(f'^({HandlerHelpers.make_teams_regex(chat_id)})$', team):
            update.message.reply_text(f'Team "{team}" wasn\'t found, try again')
            return Mention.MENTION

        members = HandlerHelpers.get_team_members(chat_id, team)

        if members:
            update.message.reply_text(
                ' '.join(members),
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
            )
        else:
            update.message.reply_text(
                'Members weren\'t found or something went wrong',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
            )

        return Mention.CHOOSING_END
