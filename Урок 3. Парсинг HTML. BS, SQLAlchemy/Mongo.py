from pymongo import MongoClient
from pprint import pprint
client = MongoClient('localhost',27017)
db = client['BD256']
users = db.users

# users.insert_many([{"author": "Mike",
#               "age" : 32,
#               "text": "Simple text",
#               "tags": ["a", "ul"],
#               "date": '03.11.2006'},
#
#                    {"author": "Eliot",
#               "age" : 56,
#               "title": "MongoDB is fun",
#               "text": "and pretty easy too!",
#               "date": '01.08.2010'}]
# )

# objects = users.find({'author':'John'},{'author','date','age'})
# objects = users.find({'age':{'$gte':10}}).sort('author').limit(3)
users.delete_one({'name':'Георгий'})

objects = users.find().sort('author')
# for obj in objects:
#     pprint(obj)

print(users.count_documents({'author':'Eliot'}))
