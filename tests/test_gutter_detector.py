import cv2
import numpy as np

from comic_splitter import gutter_detector
from comic_splitter.gutter_detector import GutterDetector
from tests.page_utils import PageUtils

utils = PageUtils()


class TestGutterDetector():

    def test_detector_with_one_panel_returns_panel(self):
        test_page = utils.generate_page([((20, 20), (40, 40))], 50, 50)
        detector = GutterDetector()
        assert detector.detect_gutters(test_page) == ()


    def test_detector_with_stacked_panels_detects_horizontal_gutter(self):
        top_panel = ((10, 10), (40, 40))
        bottom_panel = ((10, 50), (40, 90))
        test_page = utils.generate_page([top_panel, bottom_panel], 100, 50)
        utils.save_image(test_page)
        detector = GutterDetector()

        vert_gutters, horiz_gutters = detector.detect_gutters(test_page) 

        assert len(vert_gutters) == 1
        assert len(horiz_gutters) == 2 

    def test_detector_creates_xy_projection(self):
        black = (0, 0, 255)
        width, height = 50, 50
        test_page = utils.generate_page(page_height= height, page_width= width)
        cv2.line(test_page,
                 pt1 = (0, 25), pt2 = (50, 25), color = black, thickness = 1)

        detector = GutterDetector()
        vert_gutter_indices = detector._projection(test_page, 'vertical')
        horiz_gutter_indices = detector._projection(test_page, 'horizontal')

        assert vert_gutter_indices.tolist() == []
        assert horiz_gutter_indices.tolist() == [
            i for i in range(height) if i != 25]

    def test_detector_projects_nothing_given_empty_page(self):
        width, height = 50, 50
        test_page = utils.generate_page(page_height= height, page_width= width)
        detector = GutterDetector()

        vert_proj = detector._projection(test_page, 'vertical')
        horiz_proj = detector._projection(test_page, 'horizontal')

        assert vert_proj.tolist() == []
        assert horiz_proj.tolist() == []

    # test gutters with panels  i made myself
    # test gutters with polygonal panels
    # test guttest with panels with gaps
    # test gutters with panels in odd formats (overlapping, outside of page)
    # test gutters with page with no gutters!
    # test gutters are black not white (must cv2.reduce in inverse way)
    
    def test_detector_returns_central_gutter_index(self):
        gutter_indices = np.arange(0, 50)
        gutter_indices= np.delete(gutter_indices, 25)
        gutter_indices= np.delete(gutter_indices, 5)
        gutter_detector = GutterDetector()
        central_indices = gutter_detector._centralize_indices(gutter_indices)
        print('central', central_indices)
        assert central_indices == [2, 15, 37]

