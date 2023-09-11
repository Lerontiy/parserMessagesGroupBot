from pymongo.mongo_client import MongoClient

from settings import get_uri, get_password


class Database:
    def __init__(self):
        self.collection = None
        self.group_id = None

        self.collection = self.get_collection()

        info_dict = self.collection.find_one({"_id": 0})
        if info_dict is None:
            self.collection.insert_one({"_id": 0, "password": get_password(), "group_id": "0"})

        if info_dict["group_id"] != "0":
            self.group_id = info_dict["group_id"]
        del info_dict


    def get_collection(self):
        cluster = MongoClient(get_uri(), connect=False, port=27017)
        db_connect = cluster["main"]
        del cluster
        return db_connect["main"]


    def get_db_password(self):
        cluster = MongoClient(get_uri(), connect=False, port=27017)
        db_connect = cluster["main"]
        del cluster
        collection = db_connect["main"]
        collection = collection.find_one()
        return collection['password']


db = Database()






# from settings import get_password
#
# import sqlite3
#
#
# class Database:
#     def __init__(self):
#         self.path = "database.db"
#         self.make_db_not_empty()
#         self.group_id = self.findDb("SELECT group_id FROM main")
#
#     def make_db_not_empty(self):
#         with sqlite3.connect(self.path) as con:
#             cur = con.cursor()
#             if cur.execute("SELECT id_number FROM main").fetchone() is None:
#                 self.changeDb("INSERT INTO main VALUES (%s, '%s', '%s')" % (0, '0', get_password()))
#
#
#     def changeDb(self, request):
#         with sqlite3.connect(self.path) as con:
#             cur = con.cursor()
#             cur.execute(request)
#             con.commit()
#
#     def findDb(self, request):
#         with sqlite3.connect("database.db") as con:
#             cur = con.cursor()
#             return cur.execute(request).fetchone()[0]
#
#
# db = Database()
