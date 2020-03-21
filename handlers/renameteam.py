import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
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

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id

        if not HandlerHelpers.check_teams_existence(update):
            return RenameTeam.CHOOSING_END

        markup = ReplyKeyboardMarkup(map(lambda x: [x], HandlerHelpers.get_teams(chat_id)), one_time_keyboard=True)
        update.message.reply_text(
            'Choose team to rename',
            reply_markup=markup
        )

        return RenameTeam.CHOOSING_TEAM

    def choose_team(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        context.user_data['old_team_name'] = old_team_name = update.message.text

        if not re.match(f'^({HandlerHelpers.make_teams_regex(chat_id)})$', old_team_name):
            update.message.reply_text(f'Team "{old_team_name}" wasn\'t found, try again')
            return RenameTeam.CHOOSING_TEAM

        update.message.reply_text(
            f'Now send new name for the team "{old_team_name}"',
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )

        return RenameTeam.CHOOSING_NEW_NAME

    def choose_new_name(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        new_team_name = update.message.text
        old_team_name = context.user_data['old_team_name']

        if App.db.get_teams().find_one({'chat_id': chat_id, 'name': new_team_name}):
            update.message.reply_text(
                f'Team wasn\'t renamed, cause "{new_team_name}" already exists, send new name for team "{old_team_name}" again',
            )
            return RenameTeam.CHOOSING_NEW_NAME

        if not re.match(r'[a-zа-яё._-]{2,16}', new_team_name.lower(), re.IGNORECASE):
            update.message.reply_text(
                f'Team wasn\'t renamed, cause name "{new_team_name}" contains incorrect symbols, try again',
            )
            return RenameTeam.CHOOSING_NEW_NAME

        if App.db.get_teams().find_one_and_update({'chat_id': chat_id, 'name': old_team_name}, {'$set': {'name': new_team_name}}):
            update.message.reply_text(
                f'Team "{old_team_name}" was renamed to "{new_team_name}"'
            )
        else:
            update.message.reply_text(
                f'Team "{old_team_name}" wasn\'t renamed to "{new_team_name}" due to some errors, try again later',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
            )

        return RenameTeam.CHOOSING_END
