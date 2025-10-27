import os
import unittest

import cv2
import numpy as np
import pytest
from cv2.typing import MatLike

from comic_splitter.page_section import PageSection
from comic_splitter.section_detector import SectionDetector
from page_utils import PageUtils

utils = PageUtils()


class TestSectionDetector(unittest.TestCase):

    def test_detector_detects_whole_page_when_no_sections_given(self):
        test_page = utils.generate_page(rectangle_coords=[],
                                        page_height=50, page_width=50)
        detector = SectionDetector(test_page)
        sections = detector.detect_page_sections()
        assert len(sections) == 1

    def centroid_within_panel_coords(self, centroid, panel):
        x_cen, y_cen = centroid
        x_min, y_min = panel[0]
        x_max, y_max = panel[1]
        return x_min < x_cen < x_max and y_min < y_cen < y_max

    def test_detector_finds_page_section(self):
        panel_coord = ((10, 10), (40, 40))
        test_page = utils.generate_page(rectangle_coords=[panel_coord],
                                        page_height=50, page_width=50,
                                        thickness=2)
        detector = SectionDetector(test_page)

        sections = detector.detect_page_sections()
        assert len(sections) == 1
        assert self.centroid_within_panel_coords(
            sections[0].centroid, panel_coord)

    def gutter_not_in_panel_bounds(
            self, gutter: int, panels: list[tuple], vertical: bool = True):
        for (x1, y1), (x2, y2) in panels:
            if vertical and x1 < gutter < x2:
                return False
            if not vertical and y1 <= gutter <= y2:
                return False
        return True

    def test_detector_with_stacked_panels_detects_horizontal_gutter(self):
        top_panel = ((10, 10), (40, 40))
        bottom_panel = ((10, 50), (40, 90))
        panels = [top_panel, bottom_panel]
        test_page = utils.generate_page(panels,
                                        page_height=100,
                                        page_width=50)

        detector = SectionDetector(test_page)
        bounds = detector.get_page_boundaries(test_page)
        vert_gutters, horiz_gutters = detector.detect_gutters(bounds)

        assert len(vert_gutters) == 2
        assert len(horiz_gutters) == 3
        for gutter in vert_gutters:
            assert self.gutter_not_in_panel_bounds(gutter, panels)
        for gutter in horiz_gutters:
            assert self.gutter_not_in_panel_bounds(
                gutter, panels, vertical=False)

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

        # need to convert panel
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
        assert bounds.bounds == ((0, 0), (50, 0), (0, 50), (50, 50))

    def test_detector_detects_gutters_in_specified_page_bounds(self):

        top_panel = ((10, 10), (40, 40))
        bottom_panel = ((10, 50), (40, 90))
        test_page = utils.generate_page([top_panel, bottom_panel],
                                        100, 50, thickness=2)
        detector = SectionDetector(test_page)

        fullpage_bounds = detector.get_page_boundaries(test_page)
        assert fullpage_bounds.bounds == ((0, 0), (50, 0), (0, 100), (50, 100))

        vg, hg = detector.detect_gutters(fullpage_bounds)
        assert len(vg) == 2 and len(hg) == 3

        intersections = detector.get_intersections(vg, hg)
        panels = detector.get_subsections_from_intersections(intersections)
        top_panel, bottom_panel = panels[0], panels[1]

        # convert from panel to PageSection
        vg_top, hg_top = detector.detect_gutters(top_panel)
        vg_bottom, hg_bottom = detector.detect_gutters(bottom_panel)

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
        assert central_indices == [2, 15, 37]

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

    def test_get_page_sections_from_intersections(self):
        empty_page = np.full((5, 5), 255, dtype=np.uint8)
        detector = SectionDetector(empty_page)
        assert detector.get_subsections_from_intersections([]) == []

        top_panel = PageSection(
            (0, 0), (10, 0),
            (0, 10), (10, 10)
        )
        bottom_panel = PageSection(
            (0, 10), (10, 10),
            (0, 20), (10, 20)
        )
        expected_panels = [top_panel, bottom_panel]
        dummy_intersections = [
            (0, 0), (10, 0),
            (0, 10), (10, 10),
            (0, 20), (10, 20)
        ]

        panels = detector.get_subsections_from_intersections(
            dummy_intersections)
        assert panels == expected_panels

    def test_detector_identifies_empty_section(self):
        empty_page = np.full((50, 50), 255, dtype=np.uint8)  # white image
        detector = SectionDetector(empty_page)
        tl, tr, bl, br = ((0, 0), (58, 0), (0, 58), (58, 58))
        subsection = PageSection(tl, tr, bl, br)
        if not detector._section_is_empty(subsection):
            assert False

    def test_page_section_raises_exception_if_given_invalid_page(self):
        height, width, channels = 50, 50, 3
        color_image = np.ones((height, width, channels), dtype=np.uint8)
        unpadded_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        with self.assertRaisesRegex(Exception, 'image with >1 channel'):
            SectionDetector(color_image)

        with self.assertRaisesRegex(Exception, 'image without padding'):
            SectionDetector(unpadded_image)

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
        tl, tr, bl, br = ((0, 0), (53, 0), (0, 53), (53, 53))
        subsection = PageSection(tl, tr, bl, br)
        detector = SectionDetector(out_of_bounds_page)
        detector.page_boundaries = subsection

        subsections = detector.detect_page_sections()

        assert len(subsections) == 1
        assert self.centroid_within_panel_coords(
            subsections[0].centroid, out_of_bounds_panel)

    def test_gutter_detection_with_real_image(self):
        test_path = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.dirname(test_path)
        img_path = os.path.join(parent_path, "assets", 'real_gutter_test.jpg')

        test_img = cv2.imread(img_path)
        if test_img is None:
            raise FileNotFoundError
        test_img = self.pad_and_convert_greyscale_image(test_img)
        detector = SectionDetector(test_img)

        subpanels = detector.detect_page_sections()
        assert len(subpanels) == 5
