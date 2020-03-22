from telegram.ext import BaseFilter
from telegram import Message, MessageEntity

from classes.app import App

class AdminFilter(BaseFilter):
    """ Allow messages from administrators only """
    name = 'Filters.admin'

    def filter(self, message: Message) -> bool:
        if message.chat.PRIVATE:
            return True

        return message.from_user.id in {
            admin.user.id for admin in message.chat.get_administrators()
        }

class DefinedCommandFilter(BaseFilter):
    """ Prevent any running command """
    name = 'Filters.definedCommand'

    def filter(self, message: Message) -> bool:
        commands_names = list(map(lambda x: x['name'], App.handlers))
        command = message.text[1:]
        if command not in commands_names:
            message.reply_text('Unrecognized command, type /help to see list of all commands')
            return False

        return True

class CancelFilter(BaseFilter):
    """ Prevent any running command """
    name = 'Filters.cancel'

    def filter(self, message: Message) -> bool:
        return (message.entities and
                message.entities[0].type == MessageEntity.BOT_COMMAND and
                message.entities[0].offset == 0 and
                message.text == '/cancel')

class Filters():
    admin = AdminFilter()
    cancel = CancelFilter()
    defined_command = DefinedCommandFilter()

filters = Filters()
