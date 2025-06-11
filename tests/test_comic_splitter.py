import os
import cv2
import pytest
import numpy as np
import unittest

from app.comic_splitter.comic_splitter import ComicSplitter


class TestComicSplitter(unittest.TestCase):

    def test_split_page_with_no_panels(self):
        page_path = './tests/samples/test_page_empty.jpg'
        page_img = cv2.imread(page_path)
        splitter = ComicSplitter()
        panels = splitter.split_page()
        assert panels == []

    def test_get_stacked_panel_contours(self):
        page_path = './tests/samples/test_page_stack_two_panel.jpg'
        page_img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)
        splitter = ComicSplitter()

        contours = splitter.get_panel_contours(page_img) 
        assert self.contour_is_rectangle(contours)
        assert len(contours) == 2

    def test_get_panel_shapes_returns_bounding_rectangles(self):
        dummy_contour_1 = np.array([[[10, 10]], [[20, 10]],
                                    [[20, 20]], [[10, 20]]])
        dummy_contour_2 = np.array([[[30, 30]], [[40, 30]],
                                    [[40, 40]], [[30, 40]]])
        contours = [dummy_contour_1, dummy_contour_2]
        splitter = ComicSplitter()
        rects = splitter.get_panel_shapes(contours)
        assert len(rects) == 2
        assert rects[0] == (10, 10, 11, 11)  # x, y, width, height
        assert rects[1] == (30, 30, 11, 11)

    def test_labeling_two_stacked_panels(self):
        top_panel = ((150, 100), (2020, 1444))
        bottom_panel =  ((150, 1520), (2020, 2911))
        two_stacked_panels_page = self.generate_page(
            rectangle_coords=[
                top_panel, bottom_panel
            ]
        )
        splitter = ComicSplitter()
        contours = splitter.get_panel_contours(two_stacked_panels_page) 
        assert self.contour_is_rectangle(contours)

        label_rects = splitter.get_panel_shapes(contours)
        assert len(label_rects) == 2
        top_shape = label_rects[1]
        bottom_shape = label_rects[0]

        label_panel_by_index = splitter.get_indexed_panels(label_rects)
        # labeling panels from top to bottom
        assert label_panel_by_index == [top_shape, bottom_shape]

    def test_labeling_multiple_side_by_side_panels(self):
        left_panel = ((35, 35), (550, 2890))
        middle_panel = ((767, 35), (1287, 2890))
        right_panel = ((1448, 35), (1960, 2890))

        multiple_side_by_side_panels_page = self.generate_page(
            rectangle_coords=[
                left_panel, middle_panel, right_panel
            ]
        )
        splitter = ComicSplitter()
        contours = splitter.get_panel_contours(
            multiple_side_by_side_panels_page)
        assert self.contour_is_rectangle(contours)

        label_rects = splitter.get_panel_shapes(contours)
        assert len(label_rects) == 3
        left_shape, middle_shape, right_shape = (label_rects[2],
                                                 label_rects[1],
                                                 label_rects[0])

        # labeling panels from right to left
        label_panel_by_index = splitter.get_indexed_panels(label_rects)
        assert label_panel_by_index == [right_shape, middle_shape, left_shape]
    
    def test_labeling_multiple_panels(self):
        multiple_mixed_panels_page = self.generate_page(
            rectangle_coords=[
                ((1406, 100), (2100, 1515)),
                ((100, 100), (1306, 807)),
                ((100, 857), (500, 1515)),
                ((550, 857), (950, 1515)),
                ((1000, 857), (1306, 1515)),
                ((100, 1615), (2100, 2935))
            ]
        )

        splitter = ComicSplitter()
        contours = splitter.get_panel_contours(
            multiple_mixed_panels_page)
        assert self.contour_is_rectangle(contours)

        label_rects = splitter.get_panel_shapes(contours)
        assert len(label_rects) == 6

        # labeling points from right-to-left & top-to-bottom
        label_dict = splitter.get_indexed_panels(label_rects)

        assert label_dict == [(1405, 96, 699, 1423),
                              (99, 96, 1209, 715),
                              (999, 853, 311, 666),
                              (549, 853, 405, 666),
                              (99, 853, 405, 666),
                              (99, 1611, 2003, 1328)]


    def generate_page(self, rectangle_coords: list[tuple[tuple, tuple]],
                      page_height: int = 3035, page_width: int = 2150,
                      color: tuple = (0, 0, 0), thickness: int = 5):
        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for coord in rectangle_coords:
            start_xy, end_xy = coord[0], coord[1]
            cv2.rectangle(page, start_xy, end_xy,
                          color=color, thickness=thickness)
        return page

    def contour_is_rectangle(self, contours) -> bool:
        for contour in contours:
            if contour.shape[0] != 4:
                return False
        return True

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



