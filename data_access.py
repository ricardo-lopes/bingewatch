from pymongo import MongoClient
import os

mongo_client = None


def get_database():
    global mongo_client
    if mongo_client is None:
        connection = get_mongo_connection()
        mongo_client = MongoClient(connection)
    return mongo_client.alexa


def get_current_show(alexaid):
    tvshows = get_database().tvshows
    current_show = tvshows.find_one(
        {"alexaid": alexaid,
         "watching": True
         })
    return current_show


def set_show_watch_status(id, value):
    tvshows = get_database().tvshows
    result = tvshows.update_one({"_id":id}, {"$set":{'watching': value}})
    return result


def get_mongo_connection():
    return os.getenv("MONGO_CONNECTION")

# def insert_data():
#     db = get_database()
#     seinfeld = {
#         "alexaid": "testid1",
#         "name": "seinfeld",
#         "season": 10,
#         "watching": True,
#         "lastseen": None
#     }
#     dexter = {
#         "alexaid": "testid1",
#         "name": "dexter",
#         "season": 4,
#         "watching": False,
#         "lastseen": None
#     }
#     wire = {
#         "alexaid": "testid1",
#         "name": "the wire",
#         "season": 1,
#         "watching": False,
#         "lastseen": None
#     }
#     tvshows = db.tvshows
#     tvshows.insert_one(seinfeld)
#     tvshows.insert_one(dexter)
#     tvshows.insert_one(wire)