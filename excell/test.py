from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.Extract  # You can change 'admin' to your database name
    server_info = db.command('serverStatus')
    print(f"Connected to MongoDB server version {server_info['version']}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
