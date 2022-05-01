from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = process.env.MONGO_URL
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('internshala')
user_collection = pymongo.collection.Collection(db, 'internships')
