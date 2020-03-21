import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler
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

    def start(self, update, context: CallbackContext):
        markup = ReplyKeyboardMarkup(map(lambda x: [x], self.get_teams()), one_time_keyboard=True)
        update.message.reply_text(
            f'Choose a team',
            reply_markup=markup
        )

        return AddMembers.CHOOSING_TEAM

    def choose_team(self, update, context: CallbackContext):
        team = update.message.text

        if not re.match(f'^({self.make_teams_regex()})$', team):
            update.message.reply_text(f'Team "{team}" was\'t found, try again')
            return AddMembers.CHOOSING_TEAM

        context.user_data['team'] = team
        update.message.reply_text(
            f'Now, send user @logins separated by space to add them to team "{team}"',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        return AddMembers.CHOOSING_MEMBERS

    def choose_members(self, update, context: CallbackContext):
        _team = context.user_data['team']
        _members = list(
            filter(
                lambda x: x.startswith('@') and x not in self.get_team_members(_team),
                update.message.text.split(' ')
            )
        )

        if _members:
            self.add_members(_team, _members)

            update.message.reply_text(
                f'Greeting new members of the "{_team}" team: {" ".join(_members)}'
            )
        else:
            update.message.reply_text(
                f'No members were added to the team "{_team}"'
            )

        return AddMembers.CHOOSING_END

    def add_members(self, team: str, members: list):
        key = 'members'

        if key not in self.get_chat_data_teams()[team]:
            self.get_chat_data_teams()[team][key] = {}

        self.get_chat_data_teams()[team][key] = self.get_team_members(team) + members
