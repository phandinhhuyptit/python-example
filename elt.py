from pymongo import MongoClient
import pandas as pd
import sys

# Load data from CSV file
try:
    # Read the CSV file into a DataFrame
    df = pd.read_csv('mydata.csv')
except Exception as e:
    print(f'Error reading CSV file: {e}')
    sys.exit(1)
    
# Validate the data
assert df['age'].dtype == 'int' and df['age'].min() > 0, 'Invalid age data'
assert df['name'].apply(lambda x: isinstance(x, str) and len(x) > 0).all(), 'Invalid name data'
assert df['city'].apply(lambda x: isinstance(x, str) and len(x) > 0).all(), 'Invalid city data'

# Transform the data
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 65, 100], labels=['Under 18', '18-35', '35-65', 'Over 65'])
df['name_length'] = df['name'].apply(len)
# df['test'] = df['age'].apply(lambda x: x*2)

# Filter the data
df = df[df['age'] > 30]

# Aggregate the data
test = df.groupby('city')['age'].agg(['sum', 'mean', 'max'])

# Conditional data transformation
df['name_length'] = df.apply(lambda x: len(x['name']) if x['age'] > 30 else None, axis=1)

# # Conditional data filtering
# df = df[(df['age'] > 30) & (df['city'] == 'Dallas')]

# Conditional data aggregation
df[df['age'] > 30].groupby('city')['age'].mean()


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']
# Query data from the database
results = collection.find({'age': {'$gt': 30}})

# # Query data from the database with field filtering
results = collection.find({'age': {'$gt': 30}}, projection={'name': 1, 'city': 1})

# # Query data from the database with sorting
results = collection.find({'age': {'$gt': 30}}).sort('age', -1)

# New feature: Query data from the database with aggregation
pipeline = [
    {'$match': {'age': {'$gt': 30}}},
    {'$group': {'_id': '$city', 'average_age': {'$avg': '$age'}}}
]
results = collection.aggregate(pipeline)

try:
    # Insert the data into the collection
    collection.insert_many(df.to_dict('records'))
except Exception as e:
    print(f'Error writing data to database: {e}')
    sys.exit(1)