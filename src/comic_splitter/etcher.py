from typing import Literal
from cv2.typing import MatLike
import numpy as np
import cv2

from comic_splitter.page import Panel
from comic_splitter.page_section import PageSection


class Etcher:

    def etch(self, page: MatLike, panels: list[Panel],
             label: bool = False, blank: bool = False,
             mode: Literal["BORDER", "RECTANGLES"] = "BORDER") -> MatLike:

        page = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
        height, width, _ = page.shape
        canvas = np.ones(
            (height, width, 3), np.uint8) if blank else page.copy()

        red = (0, 0, 255)
        blue = (255, 0, 0)
        green = (0, 255, 0)
        colors = [red, blue, green]

        color_picker = 0
        for panel in panels:
            (x, y, w, h) = panel.get_rect()
            if color_picker == 3:
                color_picker = 0
            if mode == 'RECTANGLES':
                cv2.rectangle(canvas, (x, y), (x + w, y + h),
                              colors[color_picker], -1)
            elif mode == 'BORDER':
                cv2.rectangle(canvas, (x, y), (x + w, y + h),
                              colors[color_picker], 3)
            color_picker += 1

        if label:
            self.draw_label_contours(canvas, panels)

        return canvas

    def draw_label_contours(self, page: MatLike,
                            bounds: list[Panel] | list[PageSection]):
        for i, bound in enumerate(bounds):
            x, y, w, h = bound.get_rect()
            center_x = x + w // 2
            center_y = y + h // 2

            cv2.putText(
                page, str(i + 1),
                (center_x, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)

    def _etch_section(self, page: MatLike, rectangles: list[PageSection],
                      label: bool = False, blank: bool = False,
                      mode: Literal[
                       "BORDER", "RECTANGLES"] = "BORDER") -> MatLike:

        page = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
        height, width, _ = page.shape
        canvas = np.ones(
            (height, width, 3), np.uint8) if blank else page.copy()

        for section in rectangles:
            x, y = section.x, section.y
            w, h = section.width, section.height

            if mode == 'RECTANGLES':
                cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 255), -1)
            elif mode == 'BORDER':
                cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 255), 3)

        if label:
            self.draw_label_contours(canvas, rectangles)

        return canvas
