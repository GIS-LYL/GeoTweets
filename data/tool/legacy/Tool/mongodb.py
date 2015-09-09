from pymongo import MongoClient

# Create a connection
client = MongoClient()

# Access a database
db = client.test

# Access a collection
user = db.user

cursor = user.find()

for entry in cursor:
    print entry['name']