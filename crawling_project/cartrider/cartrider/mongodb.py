import pymongo

client = pymongo.MongoClient('mongodb server ip')
db = client.cartrider
collection = db.match