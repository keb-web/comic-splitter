from base64 import b64encode
from typing import List, Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from comic_splitter.comic_splitter import ComicSplitter
from comic_splitter.file_adapter import FileAdapter

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


# TODO: add panel size slider to frontend & feed as parameter to split
# TODO: add conversion from UploadFile to generic pythonic filetype
@app.post("/split")
async def split(mode: Literal['crop', 'etch'] = Form('crop'),
                blank: bool = Form(False),
                label: bool = Form(False),
                margins: int = Form(0),
                files: List[UploadFile] = File(...)):
    _check_valid_file_extension(files)
    options = {'blank': blank, 'label': label,
               'margins': margins, 'mode': mode}

    adapter = FileAdapter()
    files_as_bytesio = adapter.sources_to_binary_io(files)
    splitter = ComicSplitter(files_as_bytesio, options)
    file_type = files[0].content_type

    panels = await splitter.split()

    # if panels is none raise an error

    encoded_files = [b64encode(p).decode('utf-8') for p in panels]
    return {'image_type': file_type, 'images': encoded_files}


def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')
