from fastapi import File, UploadFile, HTTPException, FastAPI
from typing import List
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

# @app.post("/split")
# async def split(files: List[UploadFile] = File(...)):
#     _check_valid_file_extension(files)
#     file_type = files[0].content_type
#     # # TODO: add comic splitt functionality, need to build splitting logic 
#     #
#     # splitter = ComicSplitter(files)
#     # panels = splitter.split()
#     #
#     # # FIX: blocking implementation might need to be async
#     # encoded_files = [await b64encode(p.file.read()).decode('utf-8') for p in panels]
#     encoded_files = [b64encode(f.file.read()).decode('utf-8') for f in files]
#
#     return {'image_type': file_type, 'images': encoded_files}

@app.post("/split")
async def split(files: List[UploadFile] = File(...)):
    _check_valid_file_extension(files)
    file_type = files[0].content_type

    splitter = ComicSplitter(files)
    panels = await splitter.split()
    # encoded_files = [b64encode(p.file.read()).decode('utf-8') for p in panels]
    encoded_files = [b64encode(p).decode('utf-8') for p in panels]

    return {'image_type': file_type, 'images': encoded_files}

def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')
