from telegram import Update, ParseMode
from telegram.ext import run_async, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, Filters

from classes.handler import BaseHandler, HandlerHelpers
from classes.queue import Queue
from classes.app import App
from classes.filters import filters

class Core(BaseHandler):
    GETTING_END = range(-1, 0)

    def init(self):
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))

    @run_async
    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'I\'m *MentionerBot*\n'
            'Type /help to get list of all commands',
            parse_mode=ParseMode.MARKDOWN
        )

    @run_async
    def help(self, update: Update, context: CallbackContext):
        timeout = 120
        Queue.add(update.message.chat.id, update.message.message_id, timeout=timeout)

        message = update.message.reply_text(
            '*Commands for admins:*\n'
            '/addteam – Add team\n'
            '/addmembers – Add members to the chosen team\n'
            '/removeteam – Remove team\n'
            '/removemembers – Remove members from the chosen team\n'
            '/renameteam – Rename team to the new given name\n'
            '\n'

            '*Commands for all members:*\n'
            '/mention – Choose a team to mention\n'
            '/getteams – List of all added teams\n'
            '/help – Get some basic info about bot and commands\n'
            '/cancel – Prevent any running command\n',
            parse_mode=ParseMode.MARKDOWN
        )

        Queue.add(message.chat.id, message.message_id, timeout=timeout)
        Queue.clean(update.message.chat.id)
