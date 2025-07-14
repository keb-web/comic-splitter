import pytest
import numpy as np

from comic_splitter.etcher import Etcher

class TestEtcher:

    @pytest.fixture
    def dummy_page(self):
        return np.zeros((100, 100), dtype=np.uint8)

    def test_etch_draws_rectangle(self, dummy_page):
        etcher = Etcher()
        rectangles = [(10, 10, 30, 30)]
        
        result = etcher.etch(dummy_page, rectangles)

        assert (result[20, 20] == [0, 0, 255]).all()
