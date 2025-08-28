import numpy as np
import cv2
import pytest

from comic_splitter.panel_detector import PanelDetector
from .page_utils import PageUtils, RectUtil

utils = PageUtils()


class TestPanelDetector():

    def to_bounding_rect(self, panel: tuple) -> tuple[int, int, int, int]:
        (x1, y1), (x2, y2) = panel
        return (x1, y1, x2 - x1, y2 - y1)

    def contours_are_rectangles(self, contours) -> bool:
        for contour in contours:
            if len(contour) != 4:
                return False
        return True

    def test_detector_returns_nothing_given_empty_page(self):
        empty_page = np.empty((0, 5))
        detector = PanelDetector()
        panels = detector.detect_panels(page_section=empty_page,
                                        x_offset=0, y_offset=0)
        assert panels == []

    def test_detector_detects_page_panel(self):
        panel = RectUtil(x=20, y=20, width=250, height=450)
        dummy_page = utils.generate_page_from_rects([panel], thickness=3)

        detector = PanelDetector()
        detected_panels = detector.detect_panels(page_section=dummy_page,
                                                 x_offset=0, y_offset=0)

        assert detected_panels == [pytest.approx(panel.contour, abs=10.0)]

    def test_panel_detection_removes_small_detected_panels(self):
        big_panel = ((150, 100), (2000, 2750))
        small_panel = ((2100, 2850), (2000, 2900))
        page = utils.generate_page(rectangle_coords=[big_panel, small_panel])

        detector = PanelDetector(6000)
        panels = detector.detect_panels(page, x_offset=0, y_offset=0)
        assert len(panels) == 1
        assert panels[0] == pytest.approx(
            self.to_bounding_rect(big_panel), abs=10.0)

    def test_detector_detects_out_of_bounds_panel(self):
        out_of_bounds_panel = ((-1, -1), (2000, 2750))
        page = utils.generate_page(
            rectangle_coords=[out_of_bounds_panel])
        detector = PanelDetector()
        panels = detector.detect_panels(page, x_offset=0, y_offset=0)
        assert len(panels) == 1

    def test_panel_detection_works_with_panel_containing_gaps(self):
        panel_with_small_gap = ((150, 100), (2000, 1300))
        panel_with_large_gap = ((150, 1350), (2000, 2750))
        page_with_gap = utils.generate_page(
            rectangle_coords=[panel_with_small_gap, panel_with_large_gap])
        gap_start, gap_end = (550, 50), (600, 250)
        cv2.rectangle(page_with_gap, gap_start, gap_end, 255, -1)  # add gaps

        detector = PanelDetector()
        panels = detector.detect_panels(page_with_gap, x_offset=0, y_offset=0)
        assert len(panels) == 2
        assert panels[0] == pytest.approx(
            self.to_bounding_rect(panel_with_large_gap), abs=10.0)
        assert panels[1] == pytest.approx(
            self.to_bounding_rect(panel_with_small_gap), abs=10.0)
