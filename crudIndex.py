from pymongo import MongoClient

# Replace with your MongoDB connection URL
mongo_url = "mongodb://localhost:27017"
client = MongoClient(mongo_url)

# Connect to a specific database
db = client["crud"]

# Get a reference to the collection
persons = db["persons"]

# Create an index on the "name" field if not already created
persons.create_index("name")
persons.create_index("city")

# Insert multiple documents
documents = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "Los Angeles"},
    {"name": "Charlie", "age": 28, "city": "Chicago"},
    # Add more documents here
]

# insert_result = persons.insert_many(documents)
# print("Inserted", len(insert_result.inserted_ids), "documents")

index_info = persons.index_information()
print("Existing index names:", list(index_info.keys()))
# Find documents by name using the index
query = {"name": "Charlie"}
cursor = persons.find(query).hint("name_1")  # Use the index "name_1"


print("Found documents:")
for document in cursor:
    print(document)

# # Update a document
# update_query = {"name": "Alice"}
# update_data = {"$set": {"age": 26}}
# update_result = persons.update_one(update_query, update_data)
# print("Modified document count:", update_result.modified_count)

# # Delete a document
# delete_query = {"name": "Alice"}
# delete_result = persons.delete_one(delete_query)
# print("Deleted document count:", delete_result.deleted_count)

# Close the connection
client.close()