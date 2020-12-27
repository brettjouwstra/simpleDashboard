from fastapi import FastAPI, File, Form, UploadFile, Header, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.encoders import jsonable_encoder as JNC
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os, io
from starlette.responses import StreamingResponse, RedirectResponse
from datetime import datetime

# Local file imports
from pyfiles.app_support import today_time
from pyfiles.doc_grid import file_finder, file_saver, all_files, count_files, doc_categories
from pyfiles.admin import CustomAdmin

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

# Serving HTML & Files
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
    allow_headers=["*"]
)

# Database
client = MongoClient(CLIENT)
db = client[DB]
collection = db[COLLECTION]

# Pydantic Models - For building the Body Requests
class Document(BaseModel):
    title: str
    description: Optional[str] = None # Notice this requires the "Optional" import from "typing"
    date: str = today_time()
    sensitive: bool

# View Routes
@api.get("/", tags=['index'], response_class=HTMLResponse)
async def index(request: Request, id: int = None):
    return templates.TemplateResponse("index.html", {"request": request, 
        "id": id, 'title': TITLE, 'today_time': today_time(), 'count_files': count_files(), 'doc_cat': len(doc_categories()[0]),
        'list_cats': doc_categories()[0], 'actual_cnt': doc_categories()[1] })

@api.get("/admin", tags=['admin'], response_class=HTMLResponse)
async def admin(request: Request, id: int = None):
    return templates.TemplateResponse( "manage.html", {"request": request, "id": id, "title": TITLE, "alldata": CustomAdmin().all_mapped() })

# Data Routes /-/
# Create new document
@api.post("/-/create", tags=['create'])
async def create( request: Request, description: str = Form(...), sensitive: str = Form(...), category: str = Form(...), files: UploadFile = File(...) ):
    filename = files.filename
    the_file = files.file
    mime = files.content_type
    contents = files.file.read()
    grid_res = file_saver(filename, contents, mime)
    collection.insert_one({ 'filename_original': filename, 'type': mime, 'referencename': grid_res, 
                    'description': description, 'sensitive': sensitive, 'category': category, 'timestamp': datetime.now() })
    return RedirectResponse(url='/')

# View One Document
@api.get("/-/view/{name}", tags=['view'])
async def view(name: str, response: Response):
    response.headers["Content-Type"] = "Application/PDF"
    viewer = file_finder(name)
    return StreamingResponse(io.BytesIO(viewer), media_type="application/pdf")

# View List of Documents
@api.get("/-/all", tags=['all'])
async def alldocs():
    return all_files()