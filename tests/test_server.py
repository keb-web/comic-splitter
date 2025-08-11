from io import BytesIO

from _pytest.runner import pytest_sessionfinish
import pytest
from fastapi.testclient import TestClient

from comic_splitter.server import app
from tests.page_utils import PageUtils

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

    # TODO: add color scheming so we can verify panels
    # BUG: x, y offset are the wrong values
    @pytest.mark.skip(reason="fix later")
    def test_valid_filetype_posted_returns_split_panels_as_pages(self):
        top_panel = ((150, 100), (2020, 1444))
        bottom_panel = ((150, 1520), (2020, 2911))
        files = [utils.generate_file_form_data(
            rectangle_coords=[top_panel, bottom_panel])]
        data = {'mode': 'crop', 'label': False, 'blank': False, 'margin': 0}
        response = client.post("/split", files=files, data=data)
        assert response.status_code == 200

        data = response.json()
        assert len(data['images']) == 2

    @pytest.mark.skip(reason='fix later')
    def test_valid_filetype_posted_returns_etched_panels_as_pages(self):
        top_panel = ((150, 100), (2020, 1444))
        bottom_panel = ((150, 1520), (2020, 2911))
        files = [utils.generate_file_form_data(
            rectangle_coords=[top_panel, bottom_panel])]
        dummy_data = {'mode': 'etch', 'label': False,
                      'blank': False, 'margin': 0}

        response = client.post("/split", files=files, data=dummy_data)
        assert response.status_code == 200

        dummy_data = response.json()
        assert len(dummy_data['images']) == 1
