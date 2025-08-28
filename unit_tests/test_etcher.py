import pytest
import numpy as np

from comic_splitter.etcher import Etcher
from comic_splitter.page_section import PageSection


class TestEtcher:

    @pytest.fixture
    def dummy_page(self):
        dummy_page = np.zeros((100, 100), dtype=np.uint8)
        self.etcher = Etcher()
        yield dummy_page

    @pytest.mark.parametrize("mode", ["BORDER", "RECTANGLES"])
    def test_etch_section_draws_sections(self, mode, dummy_page):
        section = PageSection(top_left=(10, 10), top_right=(30, 10),
                              bottom_left=(10, 30), bottom_right=(30, 30))
        result = self.etcher._etch_section(dummy_page, [section], mode=mode)
        assert tuple(result[10, 10]) != (0, 0, 0)

    @pytest.mark.parametrize("mode", ["BORDER", "RECTANGLES"])
    def test_etch_draws_rectangle_bounds(self, mode, dummy_page):
        rects = (10, 10, 20, 20)
        result = self.etcher.etch(dummy_page, [rects], mode=mode)
        assert tuple(result[10, 10]) != (0, 0, 0)
