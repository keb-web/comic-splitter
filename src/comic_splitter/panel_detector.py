from collections import defaultdict
from typing import Sequence

import cv2
import numpy as np
from cv2.typing import MatLike

from comic_splitter.book import Page, PageSection


class PanelDetector:
    ''' Detect panels using computer vision contour detection
    '''

    def __init__(self, margins: int = 0, min_panel_area: int = -1):
        self.margins = margins
        self.min_panel_area = min_panel_area

    # TODO: make work with list[PageSection]
    def detect_panels(
            self, page: MatLike, x, y) -> list[tuple]:
        x_offset, y_offset = x, y
        contours = self.get_panel_contours(page)
        rects = self.get_panel_shapes(contours, page, x_offset, y_offset)
        panels = self.get_indexed_panels(rects)
        return panels

    def get_panel_contours(self, page: MatLike) -> list[np.ndarray]:

        # TODO: after sectioning,
        # disk morphology or dilate to try to fix gaps
        # or try all transformations and see what works best
        # or try solution proposed in readme
        # dilation kind of works...readme seems better solution

        edge_page = self._preprocess_image(page)

        contours, _ = cv2.findContours(
            edge_page, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # TODO: add more contour checking here

        contours = self._remove_small_contours(contours)

        return self._approximate_contours(contours)

    def _preprocess_image(self, page: np.ndarray) -> np.ndarray:

        # kernel = np.ones((10,10),np.uint8)
        # erosion_page = cv2.erode(page, kernel,iterations = 10)
        # dilate_page = cv2.dilate(erosion_page, kernel,iterations = 10)
        # blur_page = cv2.GaussianBlur(dilate_page, (5, 5), 0)

        blur_page = cv2.GaussianBlur(page, (5, 5), 0)
        thresh_page = cv2.threshold(blur_page, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        edge_page = cv2.Canny(thresh_page, 30, 200)

        return edge_page

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

    def get_panel_shapes(self,
                         contours: list[np.ndarray],
                         page: MatLike,
                         x_offset: int = 0,
                         y_offset: int = 0) -> list[tuple]:
        rects = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            rects.append(self._apply_margins(x + x_offset,
                                             y + y_offset,
                                             w, h, page))
        return rects

    def _apply_margins(self, x: int, y: int, width: int, height: int,
                       page: MatLike):
        img_width, img_height = page.shape
        if self.margins != 0:
            x = max(x - self.margins, 0)
            y = max(y - self.margins, 0)
            width = min(width + self.margins * 2, img_width - x)
            height = min(height + self.margins * 2, img_height - y)
        return ((x, y, width, height))

    def get_indexed_panels(self, panel_rects: list[tuple]) -> list[tuple]:
        # TODO: integrate variance handling
        # only works if panels are exactly lined up by y: make it at a range

        indexed_panels = []
        panels_by_y = defaultdict(list)
        for panel in panel_rects:
            panel_height = panel[1]
            panels_by_y[panel_height].append(panel)
        for panels in panels_by_y.values():
            panels_by_x = sorted(panels, key=lambda x: x[0])
            for x_panel in panels_by_x:
                indexed_panels.insert(0, x_panel)
        return indexed_panels
