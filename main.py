from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.encoders import jsonable_encoder as JNC
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# Local file imports
from pyfiles.app_support import today_time

load_dotenv()
TITLE = os.environ['TITLE']
DESCRIPTION = os.environ['DESCRIPTION']
CLIENT = os.environ['MONGO']
DB = os.environ['DATABASE']
COLLECTION = os.environ['COLLECTION']

tags_metadata = [
    {
        "name": "index",
        "description": "Homepage",
    },
    {
        "name": "create",
        "description": "Upload documents",
    },
]

api = FastAPI(
        openapi_tags=tags_metadata,
        title=TITLE,
        description=DESCRIPTION
    )

api.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="templates")

# CORS Origins
origins = [
    "*"
]

# CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
client = MongoClient(CLIENT)
db = client[DB]
collection = db[COLLECTION]

# View Routes
@api.get("/", tags=['index'], response_class=HTMLResponse)
async def index(request: Request, id: int = None):
    return templates.TemplateResponse("index.html", {"request": request, 
        "id": id, 'title': TITLE, 'today_time': today_time() })

# Data Routes /-/
@api.post("/-/create", tags=['create'])
async def create(files: UploadFile = File(...), data: str = Form(...)):
    filename = files.filename
    return {'okay': 200}