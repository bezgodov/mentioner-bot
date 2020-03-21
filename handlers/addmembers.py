import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
from classes.app import App

class AddMembers(BaseHandler):
    CHOOSING_END, CHOOSING_TEAM, CHOOSING_MEMBERS = range(-1, 2)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start, filters=App.filters.admin),
            ],
            states={
                AddMembers.CHOOSING_TEAM: [MessageHandler(Filters.text, self.choose_team)],
                AddMembers.CHOOSING_MEMBERS: [MessageHandler(Filters.text, self.choose_members)],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)],
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id

        if not HandlerHelpers.check_teams_existence(update):
            return AddMembers.CHOOSING_END

        markup = ReplyKeyboardMarkup(map(lambda x: [x], HandlerHelpers.get_teams(chat_id)), one_time_keyboard=True)
        update.message.reply_text(
            f'Choose a team',
            reply_markup=markup
        )

        return AddMembers.CHOOSING_TEAM

    def choose_team(self, update: Update, context: CallbackContext):
        context.user_data['team'] = team = update.message.text
        chat_id = update.message.chat_id

        if not re.match(f'^({HandlerHelpers.make_teams_regex(chat_id)})$', team):
            update.message.reply_text(f'Team "{team}" wasn\'t found, try again')
            return AddMembers.CHOOSING_TEAM

        update.message.reply_text(
            f'Now, send user @logins separated by space to add them to team "{team}"',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        return AddMembers.CHOOSING_MEMBERS

    def choose_members(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        team = context.user_data['team']

        members = list(
            filter(
                lambda x: re.match(r'@[a-z._-]{5,32}', x.lower(), re.IGNORECASE) and x not in HandlerHelpers.get_team_members(chat_id, team),
                update.message.text.split(' ')
            )
        )

        if members:
            App.db.get_teams().find_one_and_update({
                'chat_id': chat_id,
                'name': team,
            }, {
                '$push': {
                    'members': {
                        '$each': members,
                    },
                },
            })

            update.message.reply_text(
                f'Greeting new members of the "{team}" team: {" ".join(members)}'
            )
        else:
            update.message.reply_text(
                f'No members were added to the team "{team}"'
            )

        return AddMembers.CHOOSING_END
