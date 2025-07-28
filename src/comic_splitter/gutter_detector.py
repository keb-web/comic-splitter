from typing import Literal
import cv2
from cv2.typing import MatLike
import numpy as np
from numpy.typing import NDArray

class Panel:
    def __init__(self, bounds, x, y):
        self.bounds = bounds
        self.top_left = bounds[0]
        self.top_right = bounds[1]
        self.bottom_left = bounds[2]
        self.bottom_right = bounds[3]
        self.x_offset = x
        self.y_offset = y
        self.centroid = self._centroid(self.top_left, self.bottom_right)
        self.index = {}

    def _centroid(self, tl, br):
        x1, y1 = tl
        x2, y2 = br
        return ((x1+x2)/2, (y1+y2)/2)
    
    def set_index(self, index, type = 'lhs'):
        self.index[type] = index

    def __repr__(self):
        return f'{self.centroid}'

class GutterDetector:
    '''
    Panel Detection by Gutter
    Gutter Detection by Vertical & Horizontal Projection
    '''

    def __init__(self):
        pass


    def detect_panels(self, page: MatLike) -> list[Panel]:
        subpanels = []
        st = self.get_page_bounds(page)
        while st:
            bounds = st.pop()
            v_gutters, h_gutters, x, y = self.detect_gutters(page, bounds)
            if self._single_panel(h_gutters, v_gutters):
                subpanels.append(Panel(bounds, x, y))
            else:
                intersections = self.get_intersections(v_gutters, h_gutters)
                new_bounds = self.get_panel_bounds_from_intersections(
                    intersections)
                st.extend(new_bounds)
        return subpanels

    def _single_panel(self, h_gutters, v_gutters):
        return len(v_gutters) <= 2 and len(h_gutters) <= 2

    def detect_gutters(self, page: MatLike, bounds: tuple):
        page, x, y = self.get_bounded_page(bounds, page)

        v_proj = self._get_projection_indices(page, 'vertical')
        h_proj = self._get_projection_indices(page, 'horizontal')

        v_gutters = [gutter + x for gutter in self._centralize_indices(v_proj)]
        h_gutters = [gutter + y for gutter in self._centralize_indices(h_proj)]

        return (v_gutters, h_gutters, x, y)

    def get_page_bounds(self, page: MatLike) -> list[tuple]:
        cols, rows = len(page), len(page[0])
        top_left, top_right = (0, 0), (rows, 0)
        bottom_left, bottom_right = (0, cols), (rows, cols)
        return [(top_left, top_right, bottom_left, bottom_right)]

    def get_bounded_page(self, bounds: tuple, page: MatLike):
        x_values = [bound[0] for bound in bounds]
        y_values = [bound[1] for bound in bounds]
        x = min(x_values)
        y = min(y_values)
        height = max(y_values) - y
        width = max(x_values) - x
        page = page[y: y+height, x: x+width]
        return page, x, y

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
        panel_bounds = []
        
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
                    panel_bounds.append(tuple(panel))

        return panel_bounds


