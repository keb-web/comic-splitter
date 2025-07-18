import os
import cv2
import numpy as np
from unittest import mock

import pytest
from comic_splitter import panel_detector
from comic_splitter.panel_detector import PanelDetector
from tests.page_utils import PageUtils

# TODO: 
# - rethink how to best interface with this class
# - make PanelDetector use wrapper for cv2
# - finish last test cases

utils =  PageUtils()

class TestPanelDetector():

    def contours_are_rectangles(self, contours) -> bool:
        for contour in contours:
            if contour.shape[0] != 4:
                return False
        return True

    def test_get_panel_shapes_returns_bounding_rectangles(self):
        dummy_contour_1 = np.array([[[10, 10]], [[20, 10]],
                                    [[20, 20]], [[10, 20]]])
        dummy_contour_2 = np.array([[[30, 30]], [[40, 30]],
                                    [[40, 40]], [[30, 40]]])
        contours = [dummy_contour_1, dummy_contour_2]
        dummy_page = mock.Mock()
        dummy_page.shape = (1, 1)
        detector = PanelDetector()
        rects = detector.get_panel_shapes(contours, dummy_page)
        assert len(rects) == 2
        assert rects[0] == (10, 10, 11, 11)
        assert rects[1] == (30, 30, 11, 11)

    def test_labeling_page_with_two_stacked_panels(self):
        top_panel = ((150, 100), (2020, 1444))
        bottom_panel =  ((150, 1520), (2020, 2911))
        two_stacked_panels_page = utils.generate_page(
            rectangle_coords=[top_panel, bottom_panel])

        detector = PanelDetector()
        contours = detector.get_panel_contours(two_stacked_panels_page) 
        assert self.contours_are_rectangles(contours)

        label_rects = detector.get_panel_shapes(contours,
                                                two_stacked_panels_page)
        assert len(label_rects) == 2
        top_shape = label_rects[1]
        bottom_shape = label_rects[0]

        label_panel_by_index = detector.get_indexed_panels(label_rects)
        # labeling panels from top to bottom
        assert label_panel_by_index == [top_shape, bottom_shape]

    def test_labeling_page_with_multiple_side_by_side_panels(self):
        left_panel = ((35, 35), (550, 2890))
        middle_panel = ((767, 35), (1287, 2890))
        right_panel = ((1448, 35), (1960, 2890))

        multiple_side_by_side_panels_page = utils.generate_page(
            rectangle_coords=[
                left_panel, middle_panel, right_panel
            ]
        )
        detector = PanelDetector()
        contours = detector.get_panel_contours(
            multiple_side_by_side_panels_page)
        assert self.contours_are_rectangles(contours)

        label_rects = detector.get_panel_shapes(
            contours, multiple_side_by_side_panels_page)
        assert len(label_rects) == 3
        left_shape, middle_shape, right_shape = (label_rects[2],
                                                 label_rects[1],
                                                 label_rects[0])

        # labeling panels from right to left
        label_panel_by_index = detector.get_indexed_panels(label_rects)
        assert label_panel_by_index == [right_shape, middle_shape, left_shape]
    
    def test_labeling_page_with_multiple_panels(self):
        multiple_mixed_panels_page = utils.generate_page(
            rectangle_coords=[
                ((1406, 100), (2100, 1515)),
                ((100, 100), (1306, 807)),
                ((100, 857), (500, 1515)),
                ((550, 857), (950, 1515)),
                ((1000, 857), (1306, 1515)),
                ((100, 1615), (2100, 2935))
            ]
        )

        detector = PanelDetector()
        contours = detector.get_panel_contours(multiple_mixed_panels_page)
        assert self.contours_are_rectangles(contours)

        label_rects = detector.get_panel_shapes(contours,
                                                multiple_mixed_panels_page)
        assert len(label_rects) == 6

        # labeling points from right-to-left & top-to-bottom
        label_dict = detector.get_indexed_panels(label_rects)

        assert label_dict == [(1405, 96, 699, 1423),
                              (99, 96, 1209, 715),
                              (999, 853, 311, 666),
                              (549, 853, 405, 666),
                              (99, 853, 405, 666),
                              (99, 1611, 2003, 1328)]

    def test_labeling_page_with_multiple_nested_panels(self):
        outer_panel = ((100,100), (1200, 2900))
        slight_outer_panel = ((95,95), (1205, 2905))
        inner_panel_1 = ((200, 200), (1100, 1400))   # Top-left quarter
        panel_1_child = ((250, 250), (1000, 1200))   # inside inner_panel_1
        inner_panel_2 = ((200, 1500), (1100, 2700))  # Bottom-right
        unrelated_panel = ((1300, 95), (2000, 2900))
        nested_panel_page = utils.generate_page(
            rectangle_coords=[
                outer_panel,
                inner_panel_1,
                panel_1_child,
                inner_panel_2,
                slight_outer_panel,
                unrelated_panel
            ]
        )

        detector = PanelDetector()
        contours = detector.get_panel_contours(nested_panel_page)
        assert self.contours_are_rectangles(contours)
        assert len(contours) == 2

        label_rects = detector.get_panel_shapes(contours, nested_panel_page)
        assert len(label_rects) == 2

        # TODO: better way to test indexed panels in a readable way
        label_dict = detector.get_indexed_panels(label_rects)
        assert label_dict == [(1299, 91, 705, 2813), (94, 91, 1115, 2818)]

    def test_panel_detection_with_margin(self):
        test_page = utils.generate_page(
            rectangle_coords=[((50, 50), (200, 200))],
            page_height = 400, page_width = 400
        )
        detector = PanelDetector(margins=25)
        contours = detector.get_panel_contours(page=test_page)
        shapes = detector.get_panel_shapes(contours, test_page)
        panel = detector.get_indexed_panels(shapes)
        assert panel  == [(24, 21, 205, 208)]

    def test_panel_detection_removes_small_detected_panels(self):
        big_panel = ((150, 100), (2000, 2750))
        small_panel =  ((2100, 2850), (2000, 2900))
        two_stacked_panels_page = utils.generate_page(
            rectangle_coords=[big_panel, small_panel])

        detector = PanelDetector(min_panel_area=5701)
        contours = detector.get_panel_contours(two_stacked_panels_page) 
        assert self.contours_are_rectangles(contours)

        small_contour, big_contour = contours[0], contours[1]
        assert cv2.contourArea(small_contour) < cv2.contourArea(big_contour)

        filtered_contours = detector._remove_small_contours(contours)
        assert len(filtered_contours) == 1

    @pytest.mark.skip(reason=' issues')
    def test_panel_detects_panel_partially_out_of_bounds_of_page(self):
        out_of_bounds_panel = ((-1, -1), (2000, 2750))
        out_of_bounds_page = utils.generate_page(
            rectangle_coords=[out_of_bounds_panel])
        detector = PanelDetector()
        contours = detector.get_panel_contours(out_of_bounds_page) 
        assert self.contours_are_rectangles(contours)
        label_rects = detector.get_panel_shapes(contours, out_of_bounds_page)
        # BUG: outermost contour/rectangle not used
        assert len(label_rects) == 1

    @pytest.mark.skip('reason= test finding page borders by inverting')
    def test_panel_detection_with_page_containing_gaps(self):
        panel_with_small_gap = ((150, 100), (2000, 1300))
        panel_with_large_gap = ((150, 1350), (2000, 2750))
        page_with_gap = utils.generate_page(
            rectangle_coords=[panel_with_small_gap, panel_with_large_gap])
        gap_start, gap_end = (550, 50), (600, 250)
        cv2.rectangle(page_with_gap, gap_start, gap_end, 255, -1)

        # kernel = np.ones((10,10),np.uint8)
        # erosion_page = cv2.erode(page_with_gap, kernel,iterations = 10)
        # dilate_page = cv2.dilate(erosion_page, kernel,iterations = 10)
        # blur_page = cv2.GaussianBlur(dilate_page, (5, 5), 0)
        # vu.save_image(dilate_page)

        detector = PanelDetector()
        contours = detector.get_panel_contours(page_with_gap) 
        utils.draw_labels(page_with_gap, contours)

        assert self.contours_are_rectangles(contours)
        assert len(contours) == 2

    # integration homie!
    @pytest.mark.skip('reason= fixing other issues first so this one works')
    def test_panel_detection_with_real_test_page(self):
        test_dir = os.path.dirname(__file__)
        page_path = os.path.join(test_dir, 'samples', 'book_page.jpg')
        test_page = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)
        detector = PanelDetector()
        contours = detector.get_panel_contours(test_page)
        assert len(contours) == 3

    @pytest.mark.skip('reason= figuring stuff out')
    def test_spike_morphological_operations(self):
        # test_panel = ((150, 100), (2000, 1300))
        # dummy_page = utils.generate_page(rectangle_coords=[test_panel])
        #
        # gap_start = (550, 50)
        # gap_end = (600, 250)
        # cv2.rectangle(dummy_page, gap_start, gap_end, 255, -1)

        test_dir = os.path.dirname(__file__)
        page_path = os.path.join(test_dir, 'samples', 'book_page.jpg')
        dummy_page = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)

        kernel = np.ones((15, 15),np.uint8)

        opened = cv2.morphologyEx(dummy_page, cv2.MORPH_OPEN, kernel)
        # opened = cv2.morphologyEx(dummy_page, cv2.MORPH_CLOSE, kernel)
        utils.save_image(opened)

        # erosion_page = cv2.erode(page_with_gap, kernel,iterations = 10)
        # dilate_page = cv2.dilate(erosion_page, kernel,iterations = 10)
        # blur_page = cv2.GaussianBlur(dilate_page, (5, 5), 0)

        # detector = PanelDetector()
        # contours = detector.get_panel_contours(dummy_page) 
        # vu.draw_labels(dummy_page, contours)

    # FIX: most problems are fixed if
    #      we compare by rectangle rather than contour
    # we can remove inside rectangles to get a better depiction of our panels
    # need to find some way to optimize this, though
    # option 2: split by area between panels, then we can preprocess each
    # split to get accurate results

    # TODO:
    # def test_polygon_panel(self):
    # def test_labeling_multiple_panels_with_different_x_y():
    # def test_labeling_panels_with_context():
    # def test_labeling_inverted_panels():
    # def margin moves contour out of bounds test():
    # def fallback test, if no obvious panel is found, return whole page

