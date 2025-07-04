from io import BytesIO
from fastapi import UploadFile
from fastapi.testclient import TestClient

from comic_splitter.server import app

client = TestClient(app)

class TestAPI:
    def test_invalid_filetype_posted_returns_error(self):
        fake_image = BytesIO(b"fake image content")
        files = [("files", ("FakeFile.badtype", fake_image, "image/badtype"))]

        response = client.post("/split", files=files)

        assert response.status_code == 400
        assert response.json() == {'detail': 'invalid filetype'}


    # TODO: iterate iterate iterate!!
    def test_valid_filetype_posted_returns_split_panels_as_pages(self):
        fake_image = BytesIO(b"fake image content")
        files = [("file", ("FakeFile.png", fake_image, "image/png"))]
        response = client.post("/split", files=files)

        assert response.status_code == 200
        # assert response.json() == {'image_type': 'image/png',
        #                            'images': [files]}
        # assert zipfile returned
        # assert zipfile contents


