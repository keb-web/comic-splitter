from fastapi import File, UploadFile, HTTPException, FastAPI
from typing import List

app = FastAPI()

# Method        `POST`                                  
# Endpoint      `/upload-image`                          
# Request Body  `multipart/form-data` with 1 image file 
# Response      `application/zip` file                  


VALID_FILE_TYPES = ['jpg', 'png']

@app.post("/split")
def split(files: List[UploadFile] = File(...)):
    # for file in files:
    #     try:
    #         contents = file.file.read()
    #         with open(file.filename, 'wb') as f:
    #             f.write(contents)
    #     except Exception:
    #         raise HTTPException(status_code=500, detail='Something wrong')
    #     finally:
    #         file.file.close()
    #
    # return {"message": f"Successfuly uploaded {[]}"}    

    _check_valid_file_extension(files)
    # TODO: add comic splitt functionality, need to build splitting logic first

    return {'message': 'this is the good path'}

def _check_valid_file_extension(files: List[UploadFile]):
    for file in files:
        name = file.filename
        if name and name.rsplit('.', -1)[-1].lower() not in VALID_FILE_TYPES:
            raise HTTPException(status_code=400, detail='invalid filetype')


