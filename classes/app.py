from classes.updater import Updater
from db.mongo import Mongo

class App():
    handlers = []
    updater = Updater()
    db = Mongo()
