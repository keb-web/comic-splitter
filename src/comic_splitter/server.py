from base64 import b64encode
from typing import List, Literal

import cv2
from cv2.typing import MatLike
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
    panels_as_bytes = encode_panels_to_bytes(panels)

    # if panels is none raise an error

    encoded_files = [b64encode(p).decode('utf-8') for p in panels_as_bytes]
    return {'image_type': file_type, 'images': encoded_files}


def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')


def encode_panels_to_bytes(panel_imgs: list[MatLike], format: str = '.jpg'):
    panel_imgs_as_bytes = []
    for img_arr in panel_imgs:
        # BUG: empty panel_img slices when cropping
        if img_arr is None or img_arr.size == 0:
            print("Skipping empty image")
            continue
        success, buf = cv2.imencode(format, img_arr)
        if not success:
            raise ValueError("Failed to encode panel image")
        img_bytes = buf.tobytes()
        panel_imgs_as_bytes.append(img_bytes)

    return panel_imgs_as_bytes
