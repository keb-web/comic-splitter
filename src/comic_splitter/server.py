from base64 import b64encode
from contextlib import asynccontextmanager
from typing import Annotated, List, Literal, Sequence

import cv2
from cv2.typing import MatLike
from fastapi import Depends, FastAPI, File, Form, \
    HTTPException, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from comic_splitter.comic_splitter import ComicSplitter
from comic_splitter.config import VALID_FILE_TYPES
from comic_splitter.file_adapter import FileAdapter
import comic_splitter.db.database as db
from comic_splitter.db.models import Author, Book, Page


SessionDep = Annotated[Session, Depends(db.get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Application Startup')
    print('> Creating DB and Tables...')
    db.create_db_and_tables()
    yield
    print('Application Shutdown')

app = FastAPI(lifespan=lifespan)

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


@app.post("/split")
async def split(mode: Literal['crop', 'etch'] = Form('crop'),
                blank: bool = Form(False),
                label: bool = Form(False),
                margins: int = Form(0),
                files: List[UploadFile] = File(...)):
    _check_valid_file_extension(files)
    options = {'blank': blank, 'label': label,
               'margins': margins, 'mode': mode}
    file_type = files[0].content_type

    adapter = FileAdapter()
    files_as_bytesio = adapter.sources_to_binary_io(files)

    splitter = ComicSplitter(files_as_bytesio, options)
    panels = await splitter.split()
    panels_as_bytes = encode_panels_to_bytes(panels)
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
        if img_arr is None or img_arr.size == 0:
            print("Skipping empty image")
            continue
        success, buf = cv2.imencode(format, img_arr)
        if not success:
            raise ValueError("Failed to encode panel image")
        img_bytes = buf.tobytes()
        panel_imgs_as_bytes.append(img_bytes)

    return panel_imgs_as_bytes


@app.post("/authors/")
def create_author(author: Author, session: SessionDep) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get('/authors/')
def read_authors(
        session: SessionDep, offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,) -> Sequence[Author]:
    authors = session.exec(select(Author).offset(offset).limit(limit)).all()
    return authors


@app.get("/author/{author_id}")
def read_author(author_id: int, session: SessionDep) -> Author:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.delete("/author/{author_id}")
def delete_author(author_id: int, session: SessionDep):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}
