from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://internshala:surajcodes@cluster0.g333f.mongodb.net/internshala?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('internshala')
user_collection = pymongo.collection.Collection(db, 'internships')