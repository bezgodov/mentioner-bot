from telegram.ext import BaseFilter
from telegram import Update

class AdminFilter(BaseFilter):
    """ Allow messages from administrators only """
    name = 'Filters.admin'

    def filter(self, update: Update) -> bool:
        return update.message.from_user.id in {
            admin.user.id for admin in update.message.chat.get_administrators()
        }

class Filters():
    admin = AdminFilter()
