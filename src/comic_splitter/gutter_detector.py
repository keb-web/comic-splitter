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
    '''
    Gutter Detection by Projection
    '''

    def __init__(self):
        pass

    def get_page_bounds(self, page: MatLike):
        cols = len(page)
        rows = len(page[0])
        top_left = (0, 0)
        top_right = (rows, 0)
        bottom_left = (0, cols)
        bottom_right = (rows, cols)
        return (top_left, top_right, bottom_left, bottom_right)

    def _detect_gutters(self, page: MatLike, bounds: tuple) -> tuple:
        '''temp tree version'''

        x_values = [bound[0] for bound in bounds]
        y_values = [bound[1] for bound in bounds]
        x = min(x_values)
        y = min(y_values)
        height = max(y_values) - y
        width = max(x_values) - x
        page = page[y: y+height, x: x+width]

        v_proj = self._get_projection_indices(page, 'vertical')
        h_proj = self._get_projection_indices(page, 'horizontal')

        v_gutters = self._centralize_indices(v_proj)
        h_gutters = self._centralize_indices(h_proj)


        v_gutters = [ gutter + x for gutter in v_gutters]
        h_gutters = [ gutter + y for gutter in h_gutters]


        if len(v_gutters) == 1 and len(h_gutters) == 1:
            return ()

        return (v_gutters, h_gutters)

    def detect_gutters(self, page: MatLike) -> tuple:
        # page = self._preprocess_image(page)
        v_proj = self._get_projection_indices(page, 'vertical')
        h_proj = self._get_projection_indices(page, 'horizontal')

        v_gutters = self._centralize_indices(v_proj)
        h_gutters = self._centralize_indices(h_proj)

        if len(v_gutters) == 1 and len(h_gutters) == 1:
            return ()

        return (v_gutters, h_gutters)

    def _preprocess_image(self, page: MatLike) -> np.ndarray:
        # fails unittest
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

        # NOTE: instead of some gutter value, instead we can
        # detect the slice of pixel where a large dip/raise in sum is found
        # this will mark a gutter (raise=start, dip = end)
        # how will you determine what defines 'large?'

        # TODO:
        # we can recursive continue calling this function on cropped 
        # sections of the image until we obtain a workable solution
        # the height of the leaf determines a natural hierarchy

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
            self, indicies: np.ndarray, stepsize: int = 1) -> list:
        centers = []
        if indicies.size == 0:
            return centers
        gutter_slices = np.split(
            indicies, np.where(np.diff(indicies) != stepsize)[0]+1)
        for slice in gutter_slices:
            start = slice[0]
            center = start + int((np.max(slice) - np.min(slice)) / 2)
            centers.append(center.tolist())
        return centers
    
    def get_intersections(self, v_gutters: list,
                           h_gutters: list ) -> list[tuple]:
        ans = []
        for v in v_gutters:
            for h in h_gutters:
                ans.append((v, h))
        return ans

    def get_panel_bounds_from_intersections(self, intersections: list[tuple]):
        x = sorted(set([coord[0] for coord in intersections]))
        y = sorted(set([coord[1] for coord in intersections]))
        points = set(intersections)
        panels = []
        
        for r in range(len(y) - 1):
            panel = []
            for c in range(len(x) - 1):
                y1, y2 = y[r], y[r+1]
                x1, x2 = x[c], x[c+1]
        
                panel = [
                    (x1, y1), (x2, y1),
                    (x1, y2), (x2, y2)
                ]

                if all(p in points for p in panel):
                    panels.append(tuple(panel))

        return panels


