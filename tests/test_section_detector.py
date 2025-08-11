import os
import unittest
from unittest.mock import MagicMock

import cv2
import numpy as np
import pytest
from cv2.typing import MatLike

from comic_splitter.section_detector import SectionDetector
from tests.page_utils import PageUtils

utils = PageUtils()


class TestSectionDetector(unittest.TestCase):

    def test_detector_with_no_panels(self):
        test_page = utils.generate_page([], 50, 50)
        detector = SectionDetector(test_page)
        bounds = detector.get_page_boundaries(test_page)
        v, h, _, _ = detector.detect_gutters_and_origin(test_page, bounds)
        assert len(v) == 0 and len(h) == 0

    def test_detector_with_one_panel_returns_panel(self):
        test_page = utils.generate_page([((20, 20), (40, 40))], 50, 50)
        detector = SectionDetector(test_page)
        bounds = detector.get_page_boundaries(test_page)
        v, h, _, _ = detector.detect_gutters_and_origin(test_page, bounds)
        assert len(v) == 2 and len(h) == 2

    def test_detector_with_stacked_panels_detects_horizontal_gutter(self):
        top_panel = ((10, 10), (40, 40))
        bottom_panel = ((10, 50), (40, 90))
        test_page = utils.generate_page([top_panel, bottom_panel], 100, 50)
        detector = SectionDetector(test_page)
        bounds = detector.get_page_boundaries(test_page)
        vert_gutters, horiz_gutters, _, _ = detector.detect_gutters_and_origin(
            test_page, bounds)

        assert len(vert_gutters) == 2
        assert len(horiz_gutters) == 3

    def test_detector_detects_subpanels(self):
        top_panel_left = ((10, 10), (18, 40))
        top_panel_right = (22, 10), (40, 40)
        bottom_panel = ((10, 50), (40, 90))
        dummy_panels = [self.centroid(panel) for panel in
                        [bottom_panel, top_panel_right, top_panel_left]]
        test_page = utils.generate_page(
            [top_panel_left, top_panel_right, bottom_panel],
            page_height=100, page_width=50, thickness=1)

        detector = SectionDetector(test_page)
        detector.page = test_page  # removes border added at init
        panels = [panel.centroid for panel
                  in detector.detect_page_sections()]

        assert len(panels) == len(dummy_panels)
        for detected, expected in zip(panels, dummy_panels):
            assert detected == pytest.approx(expected, abs=5.0)

    def centroid(self, panel):
        top_left, bottom_right = panel
        x1, y1 = top_left
        x2, y2 = bottom_right
        return ((x1+x2)/2, (y1+y2)/2)

    def test_page_bounds(self):
        test_page = utils.generate_page([((20, 20), (40, 40))], 50, 50)
        detector = SectionDetector(test_page)
        bounds = detector.get_page_boundaries(test_page)
        assert bounds == ((0, 0), (50, 0), (0, 50), (50, 50))

    def test_detector_detects_gutters_in_specified_page_bounds(self):

        top_panel = ((10, 10), (40, 40))
        bottom_panel = ((10, 50), (40, 90))
        test_page = utils.generate_page([top_panel, bottom_panel],
                                        100, 50, thickness=2)
        detector = SectionDetector(test_page)

        fullpage_bounds = detector.get_page_boundaries(test_page)
        assert fullpage_bounds == ((0, 0), (50, 0), (0, 100), (50, 100))

        vg, hg, _, _ = detector.detect_gutters_and_origin(
            test_page, fullpage_bounds)
        assert len(vg) == 2 and len(hg) == 3

        intersections = detector.get_intersections(vg, hg)
        panels = detector.get_panel_bounds_from_intersections(intersections)
        top_panel, bottom_panel = panels[0], panels[1]

        vg_top, hg_top, _, _ = detector.detect_gutters_and_origin(
            test_page, top_panel)
        vg_bottom, hg_bottom, _, _ = detector.detect_gutters_and_origin(
            test_page, bottom_panel)

        assert len(vg_top) == 2 and len(hg_top) == 2
        assert vg_top == [6, 43] and hg_top == [6, 43]

        assert len(vg_bottom) == 2 and len(hg_bottom) == 2
        assert vg_bottom == [6, 43] and hg_bottom == [46, 93]

    def test_detector_creates_xy_projection(self):
        black = (0, 0, 255)
        width, height = 50, 50
        test_page = utils.generate_page(page_height=height, page_width=width)
        cv2.line(test_page,
                 pt1=(0, 25), pt2=(50, 25), color=black, thickness=1)

        detector = SectionDetector(np.full((5, 5), 255, dtype=np.uint8))

        vert_gutter_indices = detector._get_projection_indices(
            test_page, 'vertical')
        horiz_gutter_indices = detector._get_projection_indices(
            test_page, 'horizontal')

        assert vert_gutter_indices.tolist() == []
        assert horiz_gutter_indices.tolist() == [i for i in range(height)
                                                 if i != 25]

    def test_detector_projects_nothing_given_empty_page(self):
        width, height = 50, 50
        test_page = utils.generate_page(page_height=height, page_width=width)
        detector = SectionDetector(test_page)

        vert_proj = detector._get_projection_indices(test_page, 'vertical')
        horiz_proj = detector._get_projection_indices(test_page, 'horizontal')

        assert vert_proj.tolist() == []
        assert horiz_proj.tolist() == []

    def test_detector_returns_central_gutter_index(self):
        gutter_indices = np.arange(0, 50)
        gutter_indices = np.delete(gutter_indices, 25)
        gutter_indices = np.delete(gutter_indices, 5)
        empty_image = np.full((5, 5), 255, dtype=np.uint8)
        section_detector = SectionDetector(empty_image)
        central_indices = section_detector._centralize_indices(gutter_indices)
        print(central_indices)
        assert central_indices == [2, 15, 37]

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
        detector = SectionDetector(multiple_mixed_panels_page)

        bounds = detector.get_page_boundaries(multiple_mixed_panels_page)
        proj_vert, proj_horiz, _, _ = detector.detect_gutters_and_origin(
            multiple_mixed_panels_page, bounds)

        img = utils.draw_lines(multiple_mixed_panels_page,
                               horiz_lines=proj_horiz, vert_lines=proj_vert)
        utils.save_image(img, 'test')

        assert len(proj_vert) == 2
        assert len(proj_horiz) == 3

    def test_get_no_intersection_between_nonexistent_gutters(self):
        vert, horiz = [], []
        detector = SectionDetector(np.full((5, 5), 255, dtype=np.uint8))
        intersections = detector.get_intersections(vert, horiz)
        assert len(intersections) == 0
        assert intersections == []

    def test_get_intersection_between_vert_horiz_gutters(self):
        vert = [48, 2126]
        horiz = [48, 1565, 2986]
        intersection_amt = len(vert) * len(horiz)
        intersections = [(48, 48), (2126, 48), (48, 1565),
                         (2126, 1565), (48, 2986), (2126, 2986)]

        empty_page = np.full((5, 5), 255, dtype=np.uint8)
        detector = SectionDetector(empty_page)
        dummy_intersections = detector.get_intersections(vert, horiz)

        assert len(dummy_intersections) == intersection_amt
        self.assertCountEqual(dummy_intersections, intersections)

    def test_get_panels_from_intersections(self):
        empty_page = np.full((5, 5), 255, dtype=np.uint8)
        detector = SectionDetector(empty_page)
        assert detector.get_panel_bounds_from_intersections([]) == []

        top_panel = (
            (0, 0), (10, 0),
            (0, 10), (10, 10)
        )
        bottom_panel = (
            (0, 10), (10, 10),
            (0, 20), (10, 20)
        )
        expected_panels = [top_panel, bottom_panel]

        dummy_intersections = [
            (0, 0), (10, 0),
            (0, 10), (10, 10),
            (0, 20), (10, 20)
        ]
        panels = detector.get_panel_bounds_from_intersections(
            dummy_intersections)
        assert panels == expected_panels

    def pad_and_convert_greyscale_image(self, image: MatLike):
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image = cv2.copyMakeBorder(image, 4, 4, 4, 4,
                                   cv2.BORDER_CONSTANT,
                                   value=(255, 255, 255))
        return image

    def test_gutter_detection_with_panel_missing_border(self):
        out_of_bounds_panel = ((20, -20), (40, 40))
        out_of_bounds_page = utils.generate_page(
            rectangle_coords=[out_of_bounds_panel],
            page_height=45, page_width=45)
        out_of_bounds_page = self.pad_and_convert_greyscale_image(
            out_of_bounds_page)

        page_boundaries = ((0, 0), (53, 0), (0, 53), (53, 53))
        detector = SectionDetector(out_of_bounds_page)
        detector.page_boundaries = page_boundaries

        subsections = detector.detect_page_sections()
        assert len(subsections) == 1

    def test_gutter_detection_with_real_image(self):

        test_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(test_path, "assets", 'real_gutter_test.jpg')
        test_img = cv2.imread(img_path)

        test_img_top_section = test_img[0: 655]

        detector = SectionDetector(
            self.pad_and_convert_greyscale_image(test_img_top_section))
        bounds = ((0, 0), (1208, 0), (0, 663), (1208, 663))

        vg, hg, _, _ = detector.detect_gutters_and_origin(
            detector.page, bounds)

        assert len(vg) >= 2 and len(hg) >= 2

        detector = SectionDetector(
            self.pad_and_convert_greyscale_image(test_img))
        subpanels = detector.detect_page_sections()

        img = utils.draw_page_sections(detector.page, subpanels)
        utils.save_image(img, 'test_img')

        assert len(subpanels) == 3

    def test_page_section_is_empty(self):
        empty_page = np.full((50, 50), 255, dtype=np.uint8)  # white image
        detector = SectionDetector(empty_page)
        bounds = ((0, 0), (58, 0), (0, 58), (58, 58))
        if not detector._section_is_empty(bounds, 0, 0):
            assert False

    def test_page_section_checks_valid_page(self):
        height, width, channels = 50, 50, 3
        color_image = np.ones((height, width, channels), dtype=np.uint8)
        unpadded_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        with self.assertRaisesRegex(Exception, 'image with >1 channels'):
            SectionDetector(color_image)

        with self.assertRaisesRegex(Exception, 'image without padding'):
            SectionDetector(unpadded_image)

    @pytest.mark.skip(reason='testing hybrid detection approach first')
    def test_detector_with_sloped_gutters_detects_gutterline(self):
        coords = np.array([
            [20, 20], [20, 50], [40, 20],         # triangle1
            [20, 480], [140, 20], [280, 480],     # triangle2
            [160, 20], [220, 20], [300, 480]       # triangle3
        ], np.int32)
        sloped_panel_page = utils.generate_polygonal_page(
            coords, page_height=500, page_width=320)

        detector = SectionDetector(sloped_panel_page)
        bounds = detector.get_page_boundaries(sloped_panel_page)
        v, h, _, _ = detector.detect_gutters_and_origin(
            sloped_panel_page, bounds[0])

        img = utils.draw_lines(sloped_panel_page, horiz_lines=h, vert_lines=v)
        utils.save_image(img)

        assert len(h) == 2
        assert len(v) == 1

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
