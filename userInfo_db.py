from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbTil

db.userInfo.drop()

userInfo = [

    {"name": "장호진", "url": "https://ohjinn.tistory.com", "pic": ""}

]


db.userInfo.insert_many(userInfo)
