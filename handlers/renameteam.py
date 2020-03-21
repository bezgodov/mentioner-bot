import re
import copy

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler
from classes.app import App

class RenameTeam(BaseHandler):
    CHOOSING_END, CHOOSING_TEAM, CHOOSING_NEW_NAME = range(-1, 2)

    def init(self):
        handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.name, self.start, filters=App.filters.admin),
            ],
            states={
                RenameTeam.CHOOSING_TEAM: [MessageHandler(Filters.text, self.choose_team)],
                RenameTeam.CHOOSING_NEW_NAME: [MessageHandler(Filters.text, self.choose_new_name)],
            },
            fallbacks=[MessageHandler(Filters.text, self.fallback)]
        )

        self.updater.dispatcher.add_handler(handler)

    def start(self, update, context: CallbackContext):
        markup = ReplyKeyboardMarkup(map(lambda x: [x], self.get_teams()), one_time_keyboard=True)
        update.message.reply_text(
            'Choose team to rename',
            reply_markup=markup
        )

        return RenameTeam.CHOOSING_TEAM

    def choose_team(self, update, context: CallbackContext):
        old_team_name = update.message.text
        context.user_data['old_team_name'] = old_team_name

        if not re.match(f'^({self.make_teams_regex()})$', old_team_name):
            update.message.reply_text(f'Team "{old_team_name}" was\'t found, try again')
            return RenameTeam.CHOOSING_TEAM

        update.message.reply_text(
            f'Now send new name for the team "{old_team_name}"',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        return RenameTeam.CHOOSING_NEW_NAME

    def choose_new_name(self, update, context: CallbackContext):
        new_team_name = update.message.text
        old_team_name = context.user_data['old_team_name']

        if new_team_name in self.get_chat_data_teams():
            update.message.reply_text(
                f'Team was\'t renamed, cause "{new_team_name}" already exists',
            )
            return RenameTeam.CHOOSING_END

        if old_team_name in self.get_chat_data_teams():
            self.get_chat_data_teams()[new_team_name] = copy.deepcopy(self.get_chat_data_teams()[old_team_name])
            self.get_chat_data_teams().pop(old_team_name)

            update.message.reply_text(
                f'Team "{old_team_name}" was renamed to "{new_team_name}"'
            )

        return RenameTeam.CHOOSING_END
