import cv2
from cv2.gapi import mul
import numpy as np
import pytest
import unittest

from comic_splitter.gutter_detector import GutterDetector
from tests.page_utils import PageUtils

utils = PageUtils()


class TestGutterDetector(unittest.TestCase):

    def test_detector_with_one_panel_returns_panel(self):
        test_page = utils.generate_page([((20, 20), (40, 40))], 50, 50)
        detector = GutterDetector()
        v, h  = detector.detect_gutters(test_page)
        assert len(v) == 2 and len(h) == 2

    def test_detector_with_stacked_panels_detects_horizontal_gutter(self):
        top_panel = ((10, 10), (40, 40))
        bottom_panel = ((10, 50), (40, 90))
        test_page = utils.generate_page([top_panel, bottom_panel], 100, 50)
        detector = GutterDetector()

        vert_gutters, horiz_gutters = detector.detect_gutters(test_page) 

        assert len(vert_gutters) == 2
        assert len(horiz_gutters) == 3
    
    @pytest.mark.skip(reason='wip')
    def test_detector_with_sloped_gutters_detects_gutterline(self):
        coords = np.array([
            [20, 20], [20, 50], [40, 20],         # triangle1
            [20, 480], [140, 20], [280, 480],     # triangle2
            [160, 20], [220, 20], [300, 480]       # triangle3
        ], np.int32)
        sloped_panel_page = utils.generate_polygonal_page(
            coords, page_height = 500, page_width = 320)

        # utils.show_projection(sloped_panel_page, direction='horizontal')
        detector = GutterDetector()
        v, h = detector.detect_gutters(sloped_panel_page)
        assert len(h) == 2
        assert len(v) == 1

    def test_detector_creates_xy_projection(self):
        black = (0, 0, 255)
        width, height = 50, 50
        test_page = utils.generate_page(page_height= height, page_width= width)
        cv2.line(test_page,
                 pt1 = (0, 25), pt2 = (50, 25), color = black, thickness = 1)

        detector = GutterDetector()
        vert_gutter_indices = detector._get_projection_indices(
            test_page, 'vertical')
        horiz_gutter_indices = detector._get_projection_indices(
            test_page, 'horizontal')

        assert vert_gutter_indices.tolist() == []
        assert horiz_gutter_indices.tolist() == [
            i for i in range(height) if i != 25]

    def test_detector_projects_nothing_given_empty_page(self):
        width, height = 50, 50
        test_page = utils.generate_page(page_height= height, page_width= width)
        detector = GutterDetector()

        vert_proj = detector._get_projection_indices(test_page, 'vertical')
        horiz_proj = detector._get_projection_indices(test_page, 'horizontal')

        assert vert_proj.tolist() == []
        assert horiz_proj.tolist() == []

    def test_detector_returns_central_gutter_index(self):
        gutter_indices = np.arange(0, 50)
        gutter_indices= np.delete(gutter_indices, 25)
        gutter_indices= np.delete(gutter_indices, 5)
        gutter_detector = GutterDetector()
        central_indices = gutter_detector._centralize_indices(gutter_indices)
        print('central', central_indices)
        assert central_indices == [2, 15, 37]

    # test gutters with panels  i made myself
    # multiple
    def test_labeling_page_with_multiple_panels(self):
        multiple_mixed_panels_page = utils.generate_page(
            rectangle_coords=[
                ((1406, 100), (2100, 1515)),   # top_right_panel
                ((100, 100), (1306, 807)),     # top_left_panel
                ((100, 857), (500, 1515)),     # bottom_left_panel_1
                ((550, 857), (950, 1515)),     # bottom_left_panel_2
                ((1000, 857), (1306, 1515)),   # bottom_left_panel_3
                ((100, 1615), (2100, 2935))    # bottom_full_width_panel
            ]
        )
        detector = GutterDetector()

        proj_vert, proj_horiz = detector.detect_gutters(
            multiple_mixed_panels_page)

        img = utils.draw_lines(multiple_mixed_panels_page,
                         horiz_lines=proj_horiz, vert_lines=proj_vert)
        utils.save_image(img, 'test')

        assert len(proj_vert) == 2
        assert len(proj_horiz) == 3

    def test_get_no_intersection_between_nonexistent_gutters(self):
        vert, horiz = [], [] 
        detector = GutterDetector()
        intersections =  detector._get_intersections(vert, horiz)
        assert len(intersections) == 0
        assert intersections == []

    def test_get_intersection_between_vert_horiz_gutters(self):
        vert =  [48, 2126]
        horiz =  [48, 1565, 2986]
        intersection_amt = len(vert) * len(horiz)
        intersections = [(48,48), (2126, 48), (48, 1565),
                         (2126, 1565), (48, 2986), (2126, 2986)]

        detector = GutterDetector()
        dummy_intersections =  detector._get_intersections(vert, horiz)

        print(dummy_intersections)
        assert len(dummy_intersections) == intersection_amt
        self.assertCountEqual(dummy_intersections, intersections)

    @pytest.mark.skip(reason='need to add slope attrib to gutter')
    def test_get_intersection_between_sloped_vert_horiz_gutters(self):
        pass

    # nested
    # out of bounds
    # polygonal
    # gaps
    # no gutters
    # inverse colors
    # full spread
         

