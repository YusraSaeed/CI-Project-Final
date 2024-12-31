from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv("../.env")

connection_string = os.getenv("MONGODB_URI")


def save_chat(data:dict):
    data['timestamp'] = datetime.now()
    with MongoClient(connection_string) as client:
        client['laptop_database']['chat'].insert_one(data)

def fetch_chat(userid:str):
    with MongoClient(connection_string) as client:
        return list(client['laptop_database']['chat'].find({'user_id':userid}).sort('timestamp', ASCENDING))