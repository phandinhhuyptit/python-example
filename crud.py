from pymongo import MongoClient
from faker import Faker
import random
import names
from bson.objectid import ObjectId

# Replace with your MongoDB connection URL
mongo_url = "mongodb://localhost:27017"
client = MongoClient(mongo_url)
fake = Faker()

# Connect to a specific database
db = client["mydatabase"]

# Get references to two collections within the database
personCollection = db["person"]
bookCollection = db["book"]

# Get the number of documents in the collection
count = personCollection.count_documents({})


def insertPersons():
    list = []
    for x in range(100):
        document = {
            "name": names.get_full_name(),
            "age": random.randint(18, 60),
            "email": names.get_first_name() + "@gmail.com",
        }
        list.append(document)
    personCollection.insert_many(list)


def insertBooks():
    list = []
    for x in range(100):
        # Generate a random index
        index = random.randint(0, count - 1)

        # Find a random person document
        random_person = personCollection.find().skip(index).limit(1).next()

        # Get the _id of the random person document
        random_person_id = random_person["_id"]

        document = {
            "title": fake.name(),
            "category": random.choice(["A", "B", "C", "D"]),
            "price": round(random.uniform(10, 100), 2),
            "author": ObjectId(random_person_id),
        }
        list.append(document)
    bookCollection.insert_many(list)


# Query: Retrieve orders along with associated user information
pipeline = [
    (
        [
            {
                "$lookup": {
                    "from": "person",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "person",
                }
            },
            {"$unwind": "$person"},
            {
                "$match": {
                    "$or": [
                        {
                            "$and": [
                                {
                                    "person.age": {"$gte": 30},
                                    "price": {"$gte": 30},
                                    "category": {"$in": ["A", "D"]},
                                }
                            ]
                        },
                        {"$and": [{"category": {"$in": ["C"]}}]},
                    ]
                }
            },
        ]
    )
]
result = bookCollection.aggregate(pipeline)
print("result", result)

for book in result:
    print("x:", book)
    print("-------------------------")

# insertBooks()
# insertPersons()
