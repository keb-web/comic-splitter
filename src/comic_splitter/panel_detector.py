from typing import Sequence

import cv2
import numpy as np
from cv2.typing import MatLike

from comic_splitter.page import Panel


class PanelDetector:
    '''
    Detect panels using computer vision contour detection
    contours represented as a bounding rectangle: (x, y, width, height)
    '''

    def __init__(self, min_panel_area: int = -1):
        self.min_panel_area = min_panel_area

    def detect_panels(self, page_section: MatLike,
                      x_offset: int, y_offset: int) -> list[Panel]:
        if page_section.size == 0:
            return []
        # old contour-based approach
        # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # save_path = os.path.join(project_root, 'test_file.jpg')
        # cv2.imwrite(save_path, page_section)

        contours = self.get_contours(page_section)
        rects = self.get_bounding_rects(contours, x_offset, y_offset)
        panels = [Panel(*rect) for rect in rects]
        return panels

    def get_contours(self, page_section: MatLike) -> list[np.ndarray]:
        page_section = cv2.bitwise_not(page_section)
        contours, _ = cv2.findContours(
            page_section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = self._remove_small_contours(contours)
        return self._approximate_contours(contours)

    def _remove_small_contours(self, contours: Sequence[MatLike]):
        big_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.min_panel_area:
                big_contours.append(contour)
        return big_contours

    def _approximate_contours(self,
                              contours: Sequence[MatLike]) -> list[np.ndarray]:
        approximate_contours = []
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx_poly = cv2.approxPolyDP(contour, epsilon, False)
            points = approx_poly.reshape(-1, 2)
            approximate_contours.append(points)
        return approximate_contours

    def get_bounding_rects(self,
                           contours: list[np.ndarray],
                           x_offset: int = 0,
                           y_offset: int = 0) -> list[tuple]:
        rects = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            rects.append((x + x_offset, y + y_offset, w, h))
        return rects
