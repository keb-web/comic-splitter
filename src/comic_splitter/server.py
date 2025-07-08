from fastapi import File, Form, UploadFile, HTTPException, FastAPI
from typing import List, Literal
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from base64 import b64encode

from comic_splitter.comic_splitter import ComicSplitter

# rmr to compress image 

app = FastAPI()

allowed_origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)

VALID_FILE_TYPES = ['jpg', 'png', 'jpeg']

@app.post("/split")
async def split(mode: Literal['crop', 'etch'] = Form(...),
                files: List[UploadFile] = File(...)):
    _check_valid_file_extension(files)
    file_type = files[0].content_type
    splitter = ComicSplitter(files)
    panels = await splitter.split(mode=mode)
    encoded_files = [b64encode(p).decode('utf-8') for p in panels]
    return {'image_type': file_type, 'images': encoded_files}

def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')
