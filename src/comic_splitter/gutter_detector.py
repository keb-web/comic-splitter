from typing import Literal
import cv2
from cv2.typing import MatLike
import numpy as np
from numpy.typing import NDArray

from comic_splitter.book import PageSection

class GutterDetector:
    '''
    Panel Section Detection by Gutter
    Gutter Detection by Vertical & Horizontal Projection
    '''
    def detect_panel_subsection(self, page: MatLike) -> list[PageSection]:
        subpanels = []

        # TODO: have value adapt to page gutter color
        page = cv2.copyMakeBorder(page, 4, 4, 4, 4, cv2.BORDER_CONSTANT,
                                  value = (255, 255, 255))
        self.page_boundaries = self.get_page_boundaries(page)

        st = [self.page_boundaries]
        while st:
            bounds = st.pop()
            v_gutters, h_gutters, x, y = self.detect_gutters(page, bounds)
            print('vg: ', v_gutters, 'hg: ', h_gutters, 'x: ', x, 'y: ', y)

            if self._single_panel(h_gutters, v_gutters):
                subpanels.append(PageSection(bounds, x, y))
            else:
                intersections = self.get_intersections(v_gutters, h_gutters)
                print('intersecitons: ', intersections)
                new_bounds = self.get_panel_bounds_from_intersections(
                    intersections)
                print('new_bounds: ', new_bounds)
                st.extend(new_bounds)
            print('\n---\n')


        return subpanels

    def _single_panel(self, h_gutters, v_gutters):
        return len(v_gutters) <= 2 and len(h_gutters) <= 2

    def detect_gutters(self, page: MatLike, bounds: tuple):
        page, x, y = self.get_bounded_page(page, bounds)

        v_proj = self._get_projection_indices(page, 'vertical')
        h_proj = self._get_projection_indices(page, 'horizontal')
        
        print('test')

        print([gutter for gutter in self._centralize_indices(v_proj)])

        v_gutters = [gutter + x for gutter in self._centralize_indices(v_proj)
            if self._within_page_bounds((gutter + x, 0))]
        h_gutters = [gutter + y for gutter in self._centralize_indices(h_proj)
            if self._within_page_bounds((0, gutter + x))]

        return (v_gutters, h_gutters, x, y)
    
    def _within_page_bounds(self, point):
        # if self.page_boundaries == ():
        #     return False
        x, y = point
        bottom_right = self.page_boundaries[3]
        max_x, max_y = bottom_right[0], bottom_right[1]
        if 0 <= y <= max_y and 0 <= x <= max_x:
            return True
        return False

    def get_page_boundaries(self, page: MatLike) -> tuple:
        cols, rows = len(page), len(page[0])
        top_left, top_right = (0, 0), (rows, 0)
        bottom_left, bottom_right = (0, cols), (rows, cols)
        return (top_left, top_right, bottom_left, bottom_right)

    def get_bounded_page(self, page: MatLike, bounds: tuple):
        x_values = [bound[0] for bound in bounds]
        y_values = [bound[1] for bound in bounds]
        x = min(x_values)
        y = min(y_values)
        height = max(y_values) - y
        width = max(x_values) - x
        page = page[y: y+height, x: x+width]
        return page, x, y

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


