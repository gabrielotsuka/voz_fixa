import pymongo
from pymongo import *	

client = pymongo.MongoClient()
db = client.Intern_Demands
collection = db.Estagiarios


post_ids = collection.insert_many(cdi)
print(post_ids.inserted_ids)

print(db.collection_names(include_system_collections = False))
