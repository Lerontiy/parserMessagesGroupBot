from pymongo.mongo_client import MongoClient

from settings import get_uri, get_password


class Database:
    def __init__(self):
        self.collection = None
        self.group_id = None

        self.collection = self.get_collection()

        info_dict = self.collection.find_one({"_id": 0})
        if info_dict is None:
            self.collection.insert_one({"_id": 0, "password": get_password(), "group_id": 0})

        if info_dict["group_id"] != 0:
            self.group_id = info_dict["group_id"]
        del info_dict


    def get_collection(self):
        cluster = MongoClient(get_uri())
        db_connect = cluster["main"]
        del cluster
        return db_connect["main"]


db = Database()
