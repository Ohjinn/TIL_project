from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbTil
db.userInfo.drop()




db.userInfo.insert_many(userInfo)
