from collections import defaultdict
from typing import Sequence
import cv2
from cv2.typing import MatLike
import numpy as np

class PanelDetector:
    def __init__(self, page: MatLike, margin: int = 0):
        self.page = page
        self.margin = margin

    def get_panel_shapes(self, contours: list[np.ndarray]) -> list[tuple]:
        rects = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            rects.append(self._apply_margins(x, y, w, h))
        return rects

    def _apply_margins(self, x, y, width, height):
        img_width, img_height = self.page.shape
        if self.margin != 0:
            x = max(x - self.margin, 0)
            y = max(y - self.margin, 0)
            width = min(width + self.margin * 2, img_width - x)
            height = min(height + self.margin * 2, img_height - y)
        return((x, y, width, height))

    def get_panel_contours(self) -> list[np.ndarray]:
        edge_page = self._preprocess_image(self.page)
        contours, _ = cv2.findContours(
            edge_page, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return self._approximate_contours(contours)

    def _preprocess_image(self, page: np.ndarray) -> np.ndarray:
        blur_page = cv2.GaussianBlur(page, (5, 5), 0)
        thresh_page = cv2.threshold(blur_page, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        edge_page = cv2.Canny(thresh_page, 30, 200)
        return edge_page

    def _approximate_contours(self,
                              contours: Sequence[MatLike]) -> list[np.ndarray]:
        approximate_contours = []
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx_poly = cv2.approxPolyDP(contour, epsilon, False)
            points = approx_poly.reshape(-1, 2)
            approximate_contours.append(points)
        return approximate_contours

    def get_indexed_panels(self, panel_rects: list[tuple]) -> list[tuple]:
        # TODO: integrate variance handling
        # only works if panels are exactly lined up by y: make it at a range

        indexed_panels = []
        panels_by_y = defaultdict(list)
        for panel in panel_rects:
            panel_height = panel[1]
            panels_by_y[panel_height].append(panel)
        for panels in panels_by_y.values():
            panels_by_x = sorted(panels, key= lambda x: x[0])
            for x_panel in panels_by_x:
                indexed_panels.insert(0, x_panel)
        return indexed_panels

    # def get_panel_bounds(self, page: np.ndarray):
    #     black_pixels = np.all(page == [0, 0, 0], axis=-1)
    #     y_coords, x_coords = np.where(black_pixels)
    #     min_x, max_x = np.min(x_coords), np.max(x_coords)
    #     min_y, max_y = np.min(y_coords), np.max(y_coords)
    #     return [min_x, min_y, max_x, max_y]

