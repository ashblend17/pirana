import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["result"]
collection = db["student"]

unique_keys = set()  # Track unique values of yourKeyField
duplicates = []

for document in collection.find():
  key_value = document["student_id"]
  if key_value in unique_keys:
    duplicates.append(document["_id"]) # Store duplicate _id for removal
  else:
    unique_keys.add(key_value)

collection.delete_many({"_id": {"$in": duplicates}}) # Remove duplicates
