import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
from classes.app import App
from classes.queue import Queue
from classes.filters import filters

class AddMembers(BaseHandler):
    CHOOSING_END, CHOOSING_TEAM, CHOOSING_MEMBERS = range(-1, 2)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start, filters=filters.admin),
            ],
            states={
                AddMembers.CHOOSING_TEAM: [
                    CommandHandler('cancel', self.cancel),
                    MessageHandler(Filters.text & ~filters.cancel, self.choose_team),
                ],
                AddMembers.CHOOSING_MEMBERS: [
                    CommandHandler('cancel', self.cancel),
                    MessageHandler(Filters.text & ~filters.cancel, self.choose_members)
                ],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)],
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update: Update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)

        chat_id = update.message.chat.id

        if not HandlerHelpers.check_teams_existence(update):
            return AddMembers.CHOOSING_END

        markup = ReplyKeyboardMarkup(map(lambda x: [x], HandlerHelpers.get_teams(chat_id)), one_time_keyboard=True)
        message = update.message.reply_text(
            f'Choose a team',
            reply_markup=markup
        )

        Queue.add(message.chat.id, message.message_id)
        return AddMembers.CHOOSING_TEAM

    def choose_team(self, update: Update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)

        context.user_data['team'] = team = update.message.text
        chat_id = update.message.chat.id

        if not re.match(f'^({HandlerHelpers.make_teams_regex(chat_id)})$', team):
            message = update.message.reply_text(f'Team "{team}" wasn\'t found, try again')
            Queue.add(message.chat.id, message.message_id)
            return AddMembers.CHOOSING_TEAM

        message = update.message.reply_text(
            f'Now, send user @logins separated by space to add them to team "{team}"',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        Queue.add(message.chat.id, message.message_id)

        return AddMembers.CHOOSING_MEMBERS

    def choose_members(self, update: Update, context: CallbackContext):
        Queue.add(update.message.chat.id, update.message.message_id)

        chat_id = update.message.chat.id
        team = context.user_data['team']

        # set is used to remove duplicated
        members = list(
            set(filter(
                lambda x: re.match(r'^@[0-9a-z._-]{5,32}$', x.lower(), re.IGNORECASE) and x not in HandlerHelpers.get_team_members(chat_id, team),
                update.message.text.split(' ')
            ))
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

            message = update.message.reply_text(
                f'Greeting new members of the "{team}" team: {" ".join(members)}'
            )

            Queue.add(message.chat.id, message.message_id)
        else:
            message = update.message.reply_text(
                f'No members were added to the team "{team}"'
            )

            Queue.add(message.chat.id, message.message_id)

        Queue.clean(update.message.chat.id, timeout=30)
        return AddMembers.CHOOSING_END
