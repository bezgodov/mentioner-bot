from telegram.ext import run_async, CallbackContext
from classes.app import App

class Queue():
    @staticmethod
    def get(message_id, chat_id):
        return App.db.get_queue().find_one({
            'chat_id': chat_id,
            'message_id': message_id,
        })

    @staticmethod
    def get_last():
        return App.db.get_queue().findOne()

    @staticmethod
    def delete(context: CallbackContext):
        chat_id = context.job.context['chat_id']
        messages = context.job.context['messages']

        if chat_id and messages:
            for msg in messages:
                message_id = msg['message_id']

                if message_id:
                    App.updater.get_updater().bot.delete_message(chat_id, message_id)

    @staticmethod
    def add(chat_id, message_id, timeout = None):
        App.db.get_queue().insert_one({
            'chat_id': chat_id,
            'message_id': message_id,
            'timeout': timeout,
        })

    @staticmethod
    def clean(chat_id, timeout = 60):
        messages = list(App.db.get_queue().find({
            'chat_id': chat_id,
        }))

        App.updater.updater.job_queue.run_once(Queue.delete, when=timeout, context={
            'chat_id': chat_id,
            'messages': messages,
        })

        for message in messages:
            App.db.get_queue().find_one_and_delete({
                'chat_id': chat_id,
                'message_id': message['message_id'],
            })
