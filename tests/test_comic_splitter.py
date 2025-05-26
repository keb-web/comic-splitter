# from PIL import Image
import cv2
import pytest
import numpy as np

from app.comic_splitter.comic_splitter import ComicSplitter


# '/home/keb/Development/comic-splitter/samples/test_page_empty.jpg'


class TestComicSplitter:

    def test_split_page_with_no_panels(self):
        page_path = './tests/samples/test_page_empty.jpg'
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        panels = splitter.split_page(page_img)
        assert panels == []


    def test_determine_box_bounds_with_one_existing_panel(self):
        page_path = './tests/samples/test_page_one_panel.jpg'
        left, top, right, bottom = 311, 342, 1889, 2705
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        assert splitter.determine_panel_bounds(page_img) == [
            left, top, right, bottom]

    @pytest.mark.skip(reason='need determine_box() func first')
    def test_split_page_with_basic_panel(self):
        page_path = './tests/samples/test_page_one_panel.jpg'
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        # margin_value = 20
        panels = splitter.split_page(page_img)
        print()
        self.view_image(page_img)
        assert panels == [page_img]

    def view_image(self, img: np.ndarray):
        cv2.imshow('test_window', img)
        cv2.waitKey(0)

# Bottom-right: (1889, 2705)
