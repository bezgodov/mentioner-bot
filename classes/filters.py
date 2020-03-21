from telegram.ext import BaseFilter
from telegram import Message

class AdminFilter(BaseFilter):
    """ Allow messages from administrators only """
    name = 'Filters.admin'

    def filter(self, message: Message) -> bool:
        if message.chat.PRIVATE:
            return True

        return message.from_user.id in {
            admin.user.id for admin in message.chat.get_administrators()
        }

class Filters():
    admin = AdminFilter()
