from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["meetings_db"]
collection = db["meetings"]

# Example 1: Filter by room (should use hashed index)
print("▶️ Room filter explain:")
pprint(collection.find({"room": "123"}).explain())

# Example 2: Filter by start_time (should use B-tree index)
print("\n▶️ Start date filter explain:")
pprint(collection.find({"start_time": {"$gte": "2025-05-04T00:00:00"}}).explain())

# Example 3: Filter by date range (compound index test)
print("\n▶️ Club + start_time filter explain:")
pprint(collection.find({
    "club": "Snowflake",
    "start_time": {"$gte": "2025-05-04T00:00:00"}
}).explain())