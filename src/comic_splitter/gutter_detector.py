from enum import unique
from typing import Literal
import cv2
from cv2.typing import MatLike
import matplotlib.pyplot as plt
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
        # page = self._preprocess_image(page)
        v_proj = self._get_projection_indices(page, 'vertical')
        h_proj = self._get_projection_indices(page, 'horizontal')
        v_gutters = self._centralize_indices(v_proj)
        h_gutters = self._centralize_indices(h_proj)

        print('vertical, ', v_gutters)
        print('horizontal, ', h_gutters)

        if len(v_gutters) == 1 and len(h_gutters) == 1:
            return ()

        return (v_gutters, h_gutters)

    def _preprocess_image(self, page: MatLike) -> np.ndarray:
        blur_page = cv2.GaussianBlur(page, (5, 5), 0)
        thresh_page = cv2.threshold(blur_page, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        edge_page = cv2.Canny(thresh_page, 30, 200)
        return edge_page


    def _get_projection_indices(self, page: MatLike,
                 direction: Literal['vertical', 'horizontal']) -> NDArray:
        projection = self._get_projection(direction, page)

        # check for single panel page
        uniq = np.unique_counts(projection)
        if len(uniq.counts) == 1 and uniq.counts == len(page):
            return np.empty((0,0))

        # TODO: instead of some gutter value, instead we can
        # detect the slice of pixel where a large dip/raise in sum is found
        # this will mark a gutter (raise=start, dip = end)
        # how will you determine what defines 'large?'

        # a tier system will probably need to be made, larger sums
        # denoting page-wide / larger gutters whereas smaller ones
        # show gutters for smaller panels

        # TODO:
        # we can recursive continue calling this function on cropped 
        # sections of the image until we obtain a workable solution
        # the height of the leaf determines a natural hierarchy

        print('projection: ', projection)
        gutter_value = int(np.max(projection))
        gutter_indices = np.where(projection >= gutter_value)
        return gutter_indices[0]

    def _get_projection(self, direction: Literal['vertical',
                        'horizontal'], page: MatLike) -> NDArray:
        axis = 0 if direction == 'vertical' else 1
        projection = cv2.reduce(
            page, axis, cv2.REDUCE_SUM, dtype=cv2.CV_32S).flatten()
        return projection

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
    
    def _get_intersections(self, v_gutters: list,
                           h_gutters: list ) -> list[tuple]:
        ans = []
        for v in v_gutters:
            for h in h_gutters:
                ans.append((v, h))
        return ans






















