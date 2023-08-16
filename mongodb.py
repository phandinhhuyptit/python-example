from pymongo import MongoClient
import random
import names

# Replace with your MongoDB connection URL
mongo_url = "mongodb://localhost:27017"
client = MongoClient(mongo_url)

# Connect to a specific database
db = client["mydatabase"]

# Get a reference to a collection within the database
personCollection = db["person"]
bookCollection = db["book"]


def insertPersons(): 
 for x in range(100):
    person = {
       "name": names.get_full_name(),
        "age": random.randint(18,100),
        "email": names.get_first_name() + "@gmail.com"
    }
    personCollection.insert_one(person)

 
def insertBooks():
 for x in range(100): 
   book = {
        "title": names.get_full_name(),
        "category": random.choice(["A", "B", "C", "D"]),
        "price": round(random.uniform(10, 100),2)
   }
   print("book",book) 

insertBooks()