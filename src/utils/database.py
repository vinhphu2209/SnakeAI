# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# class SnakeDB:
#     def __init__(self):
#         self.uri = "mongodb+srv://huukhoa04:huukhoa123@snakedb.gq6me.mongodb.net/?retryWrites=true&w=majority&appName=SnakeDB"
#         self.client = MongoClient(self.uri, server_api=ServerApi('1'))
#         self.db = self.client["SnakeDB"]
#         self.collection = self.db["SnakeCollection"]

#     def GetAllCollection(self):
#         return self.client.list_database_names()

#     def insert_document(self, name, score):
#         # Insert a new document
#         document = {"name": name, "score": score}
#         self.collection.insert_one(document)
#         print("Document inserted!")

#     def get_all_documents(self):
#         # Get all documents
#         documents = self.collection.find()
#         return list(documents)
    
#     def get20highestscore(self):
#         documents = self.collection.find().sort("score", -1).limit(20)
#         return list(documents)

# # Example usage:
# snake_db = SnakeDB()
# snake_db.insert_document("Player1", 100)
# snake_db.get_all_documents()