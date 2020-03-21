from classes.updater import Updater
from classes.filters import Filters
from db.mongo import Mongo

class App():
    updater = Updater()
    filters = Filters()
    db = Mongo()
