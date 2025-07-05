# # Setup MongoDB here
#
#
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
#
# uri = "mongodb+srv://jainish:Jainish123@requests.bt0nhtp.mongodb.net/?retryWrites=true&w=majority&appName=Requests"
#
# # Create a new client and connect to the server
# mongo = MongoClient(uri, server_api=ServerApi('1'))
#
# # Send a ping to confirm a successful connection
# try:
#     mongo.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
#
#

from flask_pymongo import PyMongo

mongo = PyMongo(uri="mongodb+srv://jainish:Jainish123@requests.bt0nhtp.mongodb.net/?retryWrites=true&w=majority&appName=Requests")