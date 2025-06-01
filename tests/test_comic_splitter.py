import os
from PIL import Image
import sys
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
        panels = splitter.split_page()
        assert panels == []

    def test_get_multiple_panel_contours(self):
        page_path = './tests/samples/test_page_stack_two_panel.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)
        splitter = ComicSplitter()

        contours = splitter.get_panel_contours(page_img) 

        top_panel_vertices = contours[0].shape[0]
        bottom_panel_vertices = contours[1].shape[0]

        assert len(contours) == 2
        assert top_panel_vertices == 4
        assert bottom_panel_vertices == 4

    @pytest.mark.skip(reason='testing another imaging approach')
    def test_determine_box_bounds_with_multiple_existing_panel(self):
        page_path = './tests/samples/test_page_one_panel.jpg'
        splitter = ComicSplitter()
        # splitter.get_panel_bounds(page_)

    @pytest.mark.skip(reason='testing another imaging approach')
    def test_determine_box_bounds_with_one_existing_panel(self):
        page_path = './tests/samples/test_page_one_panel.jpg'
        left, top, right, bottom = 311, 342, 1889, 2705
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        assert splitter.get_panel_bounds(page_img) == [
            left, top, right, bottom]


    @pytest.mark.skip(reason='need determine_box() func first')
    def test_split_page_with_basic_panel(self):
        page_path = './tests/samples/test_page_one_panel.jpg'
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        panels = splitter.split_page()
        assert panels == [page_img]

    # TODO: refactor utility functions

    def view_image(self, img: np.ndarray):
        cv2.imshow('test_window', img)
        cv2.waitKey(0)
    
    def save_image(self, img: np.ndarray, filename: str = 'debug_output'):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        save_path = os.path.join(project_root, f'{filename}.jpg')
        cv2.imwrite(save_path, img)
