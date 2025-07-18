from enum import unique
from typing import Literal
import cv2
from cv2.typing import MatLike
import numpy as np
from numpy.typing import NDArray

# NOTE: gutter detection bc contours r messy
# the plan
# preprocess
# invert to white gutters if needed (calc tot avg color?)
# gutter detection with horiz/vert projection
# save intersections

class GutterDetector:

    def __init__(self):
        pass

    def detect_gutters(self, page: MatLike) -> tuple:
        page = self._preprocess_image(page)
        v_proj = self._projection(page, 'vertical')
        h_proj = self._projection(page, 'horizontal')
        v_gutters = self._centralize_indices(v_proj)
        h_gutters = self._centralize_indices(h_proj)
        if len(v_gutters) == 1 and len(h_gutters) == 1:
            return ()
        return (v_gutters, h_gutters)

    def _preprocess_image(self, page: MatLike) -> np.ndarray:
        blur_page = cv2.GaussianBlur(page, (5, 5), 0)
        thresh_page = cv2.threshold(blur_page, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        edge_page = cv2.Canny(thresh_page, 30, 200)
        return edge_page

    def _projection(self, page: MatLike,
                 direction: Literal['vertical', 'horizontal']) -> NDArray:
        axis = 0 if direction == 'vertical' else 1
        projection = cv2.reduce(
            page, axis, cv2.REDUCE_SUM, dtype=cv2.CV_32S).flatten()

        # check for single panel page
        uniq = np.unique_counts(projection)
        if len(uniq.counts) == 1 and uniq.counts == len(page):
            return np.empty((0,0))

        gutter_value = int(np.max(projection))
        gutter_indices = np.where(projection >= gutter_value)
        return gutter_indices[0]

    def _centralize_indices(
            self, indicies: np.ndarray, stepsize: int = 1) -> list[int]:
        gutter_slices = np.split(
            indicies, np.where(np.diff(indicies) != stepsize)[0]+1)
        centers = []
        for slice in gutter_slices:
            start = slice[0]
            center = start + int((np.max(slice) - np.min(slice)) / 2)
            centers.append(center.tolist())
        return centers

