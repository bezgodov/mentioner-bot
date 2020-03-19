import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler

class Mention(BaseHandler):
    CHOOSING_END, MENTION = range(-1, 1)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start),
            ],
            states={
                Mention.MENTION: [
                    MessageHandler(Filters.text, self.mention),
                ],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)],
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update, context: CallbackContext):
        markup = ReplyKeyboardMarkup(map(lambda x: [x], self.get_teams()), one_time_keyboard=True)
        update.message.reply_text(
            f'Choose a team',
            reply_markup=markup
        )

        return Mention.MENTION

    def mention(self, update, context: CallbackContext):
        team = update.message.text
        _members = self.get_team_members(team)

        if not re.match(f'^({self.make_teams_regex()})$', team):
            update.message.reply_text(f'Team "{team}" was\'t found, try again')
            return Mention.MENTION

        if _members:
            update.message.reply_text(' '.join(_members))
        else:
            update.message.reply_text(
                'Members were\'t found or something went wrong',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
            )

        return Mention.CHOOSING_END
