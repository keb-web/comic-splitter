from fastapi import File, UploadFile, HTTPException, FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware

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

VALID_FILE_TYPES = ['jpg', 'png']


@app.post("/split")
def split(files: List[UploadFile] = File(...)):
    return {'message': 'this is the good path'}
    _check_valid_file_extension(files)
    print('here')

    # for file in files:
    #     try:
    #         contents = file.file.read()
    #         with open(file.filename, 'wb') as f:
    #             f.write(contents)
    #     except Exception:
    #         raise HTTPException(status_code=500, detail='Something wrong')
    #     finally:
    #         file.file.close()

    # return {"message": f"Successfuly uploaded {[]}"}    

    # TODO: add comic splitt functionality, need to build splitting logic first

    return {'message': 'this is the good path'}

def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')



