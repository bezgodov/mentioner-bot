from typing import Union
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from classes.config import get_config

class Mongo():
    def __init__(self):
        self.config = get_config()
        self.client = MongoClient(
            f"mongodb://{self.config['MONGO_USERNAME']}:{self.config['MONGO_PASSWORD']}@{self.config['MONGO_HOST']}:{self.config['MONGO_PORT']}"
        )
        self.create()

    def create(self):
        collection_name = self.config['MONGO_COLLECTION_NAME']
        if collection_name not in self.get_db().list_collection_names():
            self.get_db().create_collection(collection_name)

        self.get_teams().create_index('name')

    def get_db(self, db_name: Union[str, None]=None) -> Database:
        return self.client.get_database(db_name if db_name else self.config['MONGO_DB_NAME'])

    def get_teams(self) -> Collection:
        return self.get_db()[self.config['MONGO_COLLECTION_NAME']]

    def get_queue(self) -> Collection:
        return self.get_db()['queue']
