from io import BytesIO
import cv2
from fastapi import UploadFile
from fastapi.testclient import TestClient
import numpy as np

from comic_splitter.server import app

client = TestClient(app)

class TestAPI:
    def test_invalid_filetype_posted_returns_error(self):
        fake_image = BytesIO(b"fake image content")
        files = [("files", ("FakeFile.badtype", fake_image, "image/badtype"))]

        response = client.post("/split", files=files)

        assert response.status_code == 400
        assert response.json() == {'detail': 'invalid filetype'}


    # TODO: refactor into util parent class
    def generate_page(self, rectangle_coords: list[tuple[tuple, tuple]],
              page_height: int = 3035, page_width: int = 2150,
              color: tuple = (0, 0, 0), thickness: int = 5):

        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for top_left, bottom_right in rectangle_coords:
            cv2.rectangle(page, top_left, bottom_right,
                          color=color, thickness=thickness)
        return page

    # TODO: iterate iterate iterate!!
    def test_valid_filetype_posted_returns_split_panels_as_pages(self):
        top_panel = ((150, 100), (2020, 1444))
        bottom_panel =  ((150, 1520), (2020, 2911))
        two_stacked_panels_page = self.generate_page(
            rectangle_coords=[
                top_panel, bottom_panel
            ]
        )

        _, encoded_img = cv2.imencode('.png', two_stacked_panels_page)
        fake_image = BytesIO(encoded_img.tobytes())

        files = [("files", ("FakeFile.png", fake_image, "image/png"))]
        response = client.post("/split", files=files)

        data = response.json()

        assert response.status_code == 200
        assert len(data['images']) == 2
