from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
TITLE = os.environ['TITLE']
DESCRIPTION = os.environ['DESCRIPTION']
CLIENT = os.environ['MONGO']
DB = os.environ['DATABASE']
COLLECTION = os.environ['COLLECTION']


class CustomAdmin:
    def __init__(self):
        self.client = MongoClient(CLIENT)
        self.db = self.client[DB]
        self.collection = self.db[COLLECTION]

    def all_mapped(self):
        search = self.collection.find()
        results = [x for x in search]
        return results

