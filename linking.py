from pymongo import MongoClient

client = MongoClient("mongodb+srv://rsb:dbpass@rsbcluster.pf0zwp8.mongodb.net/")
db = client['Book']
collection=db['BookData']
print(collection.find_one())