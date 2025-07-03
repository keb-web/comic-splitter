from fastapi import File, UploadFile, HTTPException, FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from base64 import b64encode

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
#
# @app.post("/split")
# def split(files: List[UploadFile] = File(...)):
#     _check_valid_file_extension(files)
#
#     # for file in files:
#     #     try:
#     #         contents = file.file.read()
#     #         with open(file.filename, 'wb') as f:
#     #             f.write(contents)
#     #     except Exception:
#     #         raise HTTPException(status_code=500, detail='Something wrong')
#     #     finally:
#     #         file.file.close()
#
#     # return {"message": f"Successfuly uploaded {[]}"}    
#
#
#     with open("./lantern.JPEG", "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     print(encoded_string)
#     return [encoded_string]
#
#     # TODO: add comic splitt functionality, need to build splitting logic 

def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')

@app.post("/split")
async def split(files: List[UploadFile] = File(...)):
    # filedata = files[0].file.read()
    # filedata = base64.b64encode(filedata).decode('utf-8')

    file_type = files[0].content_type
    encoded_files = [b64encode(f.file.read()).decode('utf-8') for f in files]
    return {'image_type': file_type, 'images': encoded_files}


