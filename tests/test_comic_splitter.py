import os
import cv2
import pytest
import numpy as np

from app.comic_splitter.comic_splitter import ComicSplitter

class TestComicSplitter:

    def test_get_stacked_panel_contours(self):
        page_path = './tests/samples/test_page_stack_two_panel.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)
        splitter = ComicSplitter()

        contours = splitter.get_panel_contours(page_img) 
        assert self.contour_is_rectangle(contours)
        assert len(contours) == 2

    def test_labeling_two_stacked_panels(self):
        page_path = './tests/samples/test_page_stack_two_panel.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)

        splitter = ComicSplitter()
        contours = splitter.get_panel_contours(page_img) 
        assert self.contour_is_rectangle(contours)
        label_dict = splitter.label_contours(page_img, contours)

        # labeling panels from top to bottom
        assert label_dict == {2: contours[0], 1: contours[1]}
        assert len(contours) == 2

    def test_labeling_multiple_side_by_side_panels(self):
        page_path = './tests/samples/test_page_side_by_side.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)
        splitter = ComicSplitter()

        contours = splitter.get_panel_contours(page_img) 
        assert self.contour_is_rectangle(contours)

        # label_dict = splitter.label_contours(page_img, contours)
        # assert label_dict == {1: contours[0], 2: contours[1], 3: contours[2]}
        # assert len(contours) == 3 

    def contour_is_rectangle(self, contours) -> bool:
        for contour in contours:
            if contour.shape[0] != 4:
                return False
        return True

    @pytest.mark.skip(reason='implementing right to left first')
    def test_labeling_multiple_panels(self):
        page_path = './tests/samples/test_page_multiple_panels.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)

        splitter = ComicSplitter()
        contours = splitter.get_panel_contours(page_img) 
        label_dict = splitter.label_contours(page_img, contours)

        # self.draw_labels(page_img, contours, splitter)

        # labeling panels from top to bottom & right to left
        assert len(contours) == 6
        assert label_dict == {2: contours[0], 1: contours[1]}

    # TODO: refactor utility functions
    # NOTE: -- Utility functions --

    def draw_labels(self, img, contours, splitter):
        height, width = img.shape
        empty_image = np.zeros((height, width), dtype=np.int8)
        labeled_image = splitter.draw_contour(empty_image, contours, True)
        self.save_image(labeled_image)

    def view_image(self, img: np.ndarray):
        cv2.imshow('test_window', img)
        cv2.waitKey(0)
    
    def save_image(self, img: np.ndarray,
                   filename: str = 'debug_output'):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        save_path = os.path.join(project_root, f'{filename}.jpg')
        cv2.imwrite(save_path, img)


    # FIX: -- test below is doo doo dookie!! --

    @pytest.mark.skip('pending other test completions')
    def test_split_page_with_no_panels(self):
        page_path = './tests/samples/test_page_empty.jpg'
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        panels = splitter.split_page()
        assert panels == []


    @pytest.mark.skip(reason='adding labeling images first')
    def test_get_multiple_panel_contours(self):
        page_path = './tests/samples/test_page_multiple_panels.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)
        splitter = ComicSplitter()
        contours = splitter.get_panel_contours(page_img) 

        # TODO: add labeling to ensure vertices are correct
        # top_panel_vertices = contours[0].shape[0]
        # bottom_panel_vertices = contours[1].shape[0]
        print(contours)

        assert False
        assert len(contours) == 6
        # assert top_panel_vertices == 4
        # assert bottom_panel_vertices == 4



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
