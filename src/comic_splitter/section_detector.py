from typing import Literal

import cv2
import numpy as np
from cv2.typing import MatLike
from numpy.typing import NDArray

from comic_splitter.page_section import PageSection


class SectionDetector:
    ''' Detect PageSections by intersection of Vertical and Horizontal Gutters
        using horizontal and vertical projections
    '''

    def __init__(self, page):
        # self._verify_page_channel_and_border(page)
        self.page = page
        self.page_boundaries = self.get_page_boundaries(page)

    def _verify_page_channel_and_border(self, page: MatLike):
        if len(page.shape) == 3:
            _, _, channels = page.shape
        else:
            channels = 1
        if channels > 1:
            raise Exception('Attempt detection of image with >1 channel')
        elif self._border_exists(page) is False:
            raise Exception('Attempt detection of image without padding')

    def _border_exists(self, page: MatLike, pixel_value: int = 255):
        h, w = page.shape
        first_column = (page[0: h, 0] == pixel_value)
        last_column = (page[0: h, w-1] == pixel_value)
        first_row = (page[0] == pixel_value)
        last_row = (page[-1] == pixel_value)
        page_borders = (first_column, last_column, first_row, last_row)
        padding = np.concatenate(page_borders)
        if np.all(padding):
            return True
        return False

    def detect_page_sections(self) -> list[PageSection]:
        subsections = []
        st = [self.page_boundaries]
        while st:
            page_subsection = st.pop()
            v_gutters, h_gutters = self.detect_gutters(page_subsection)
            if v_gutters == [] and h_gutters == []:
                return [page_subsection]

            if (self._single_panel(h_gutters, v_gutters) and
                    not self._section_is_empty(page_subsection)):
                subsections.append(page_subsection)
            else:
                intersections = self.get_intersections(v_gutters, h_gutters)
                new_subsections = self.get_subsections_from_intersections(
                    intersections)
                st.extend(new_subsections)
        return subsections

    def _single_panel(self, h_gutters, v_gutters):
        return len(v_gutters) == 2 and len(h_gutters) == 2

    def _section_is_empty(self, subsection: PageSection, empty_value=255):
        region = self.page[subsection.get_slice()]
        return np.all(region == empty_value)

    def detect_gutters(self, subsection: PageSection):
        x, y = subsection.x, subsection.y
        page_section = self.page[subsection.get_slice()]

        v_proj = self._get_projection_indices(page_section, 'vertical')
        h_proj = self._get_projection_indices(page_section, 'horizontal')

        v_gutters = [gutter + x for gutter in self._centralize_indices(v_proj)
                     if self._within_page_bounds((gutter + x, 0))]
        h_gutters = [gutter + y for gutter in self._centralize_indices(h_proj)
                     if self._within_page_bounds((0, gutter + y))]

        return v_gutters, h_gutters

    def _within_page_bounds(self, point):
        x, y = point
        bottom_right = self.page_boundaries.bottom_right
        max_x, max_y = bottom_right[0], bottom_right[1]
        if 0 <= y <= max_y and 0 <= x <= max_x:
            return True
        return False

    def get_page_boundaries(self, page: MatLike) -> PageSection:
        cols, rows = len(page), len(page[0])
        top_left, top_right = (0, 0), (rows, 0)
        bottom_left, bottom_right = (0, cols), (rows, cols)
        subsection = PageSection(top_left=top_left,
                                 top_right=top_right,
                                 bottom_left=bottom_left,
                                 bottom_right=bottom_right)
        return subsection

    def _get_projection_indices(
            self, page: MatLike,
            direction: Literal['vertical', 'horizontal']) -> NDArray:

        projection = self._get_projection(direction, page)

        # check for single panel page
        uniq = np.unique_counts(projection)
        if len(uniq.counts) == 1 and uniq.counts == len(page):
            return np.empty((0, 0))

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
                          h_gutters: list) -> list[tuple]:
        ans = []
        for v in v_gutters:
            for h in h_gutters:
                ans.append((v, h))
        return ans

    def get_subsections_from_intersections(
            self, intersections: list[tuple]) -> list[PageSection]:
        x = sorted(set([coord[0] for coord in intersections]))
        y = sorted(set([coord[1] for coord in intersections]))
        points = set(intersections)
        subsections = []

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
                    tl, tr, bl, br = panel
                    subsection = PageSection(tl, tr, bl, br)
                    subsections.append(subsection)

        return subsections
