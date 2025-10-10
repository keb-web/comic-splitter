import base64
from io import BytesIO

from fastapi.testclient import TestClient

from comic_splitter.server import app
from .page_utils import PageUtils



client = TestClient(app)
utils = PageUtils()


class TestServer:

    def test_invalid_filetype_posted_returns_error(self):
        fake_image = BytesIO(b"fake image content")
        data = {'mode': 'crop'}
        files = [("files", ("FakeFile.badtype", fake_image, "image/badtype"))]

        response = client.post("/split", files=files, data=data)
        assert response.status_code == 400
        assert response.json() == {'detail': 'invalid filetype'}

    def data_is_decodable(self, image_data: str):
        decoded_file = base64.b64decode(image_data)
        return (isinstance(decoded_file, (bytes, bytearray))
                and len(decoded_file) > 0)

    def test_server_splits_valid_comic_panel(self):
        top_panel = ((150, 100), (2020, 1444))
        bottom_panel = ((150, 1520), (2020, 2911))
        files = [utils.generate_file_form_data(
            rectangle_coords=[top_panel, bottom_panel])]
        crop_payload = {'mode': 'crop', 'label': False,
                        'blank': False, 'margin': 0}
        etch_payload = {'mode': 'etch', 'label': False,
                        'blank': False, 'margin': 0}

        crop_response = client.post("/split", files=files, data=crop_payload)
        etch_response = client.post("/split", files=files, data=etch_payload)
        payload = crop_response.json()
        assert crop_response.status_code == 200
        assert len(payload['images']) == 2
        assert "images" in payload
        assert isinstance(payload["images"], list)
        first_image = payload["images"][0]
        assert isinstance(first_image, str)
        assert self.data_is_decodable(first_image)

        payload = etch_response.json()
        assert len(payload['images']) == 1


class TestServerDatabaseEndpoints:
    def test_create_book_with_pages(self):
        payload = {
                'author': 'dummy-author',
                'title': 'dummy-comic',
                'entry_number': '1',
                'pages': [
                    {
                        'page_number': 1,
                        'panels': [
                            {
                                'x': 5,
                                'y': 5,
                                'width': 20,
                                'height': 30,
                                'rtl_idx': 2,
                                'ltr_idx': 1,
                                'centroid': (15.0, 20.0)
                            },
                            {
                                'x': 25,
                                'y': 5,
                                'width': 20,
                                'height': 30,
                                'rtl_idx': 1,
                                'ltr_idx': 2,
                                'centroid': (35.0, 20.0)
                            }
                        ],
                    },
                ],
            }
        client = TestClient(app)
        response = client.post(
            "/books", json=payload
        )
        data = response.json()
        assert response.status_code == 200
        assert data["author"] == "dummy-author"
