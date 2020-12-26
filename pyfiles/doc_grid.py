from gridfs import GridFS
from pymongo import MongoClient
from dotenv import load_dotenv
import os, uuid
from bson.json_util import dumps
import io

load_dotenv()
CLIENT = os.environ['MONGO']
DATABASE = os.environ['DATABASE']
COLLECTION = os.environ['COLLECTION']

# Database
client = MongoClient(CLIENT)
db = client[DATABASE]
collection = db[COLLECTION]
grid_fs = GridFS(db)

def file_saver(filename, filedata, content_type):
    in_file = filename.split("/")[-1]
    ext = in_file.split('.')[-1]
    object_name = "{}.{}".format(str(uuid.uuid4()), ext)

    with grid_fs.new_file(filename=object_name, encoding="utf-8", content_type=content_type) as fp:
        fp.write(filedata) # Explans why encoding needed here but not when suing flask https://stackoverflow.com/questions/48368896/pymongo-gridfs-put-type-attribute-errors
        file_id = fp._id
    
    if grid_fs.find_one(file_id) is not None:
        return object_name #dumps(grid_fs.find_one(file_id))

def file_finder(name):
    grid_fs_file = grid_fs.find_one({'filename': name}, no_cursor_timeout=True)
    response = grid_fs_file.read()
    #pdf = response.decode('ISO-8859–1')
    return response

def all_files():
    meta_all = collection.find()
    return dumps(meta_all)

def count_files():
    all_grid_files = grid_fs.list()
    val = len(all_grid_files)
    return val

def doc_categories():
    all_items = collection.find()

    cats = []
    cats_o = {}
    for item in all_items:
        if item['category'] not in cats:
            cats.append(item['category'])
    
    for cnt in cats:
        val = collection.count_documents({"category": cnt})
        cats_o[cnt] = val
    return cats, cats_o
    