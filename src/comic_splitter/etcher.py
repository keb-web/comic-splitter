from typing import Literal
import numpy as np
import cv2
from numpy.typing import NDArray


class Etcher:

    def etch(self, page: np.ndarray, rectangles: list,
             label: bool = False, blank: bool = False,
             mode: Literal["BORDER", "RECTANGLES"] = "RECTANGLES" ) -> NDArray:

        page = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
        height, width, _ = page.shape
        canvas = np.ones((height,width,3), np.uint8) if blank else page.copy()

        for (x, y, w, h) in rectangles:
            if mode == 'RECTANGLES':
                cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 255), -1)
            elif mode == 'BORDER':
                cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 255), 3)

        if label:
            self.draw_label_contours(canvas, rectangles)

        return canvas

    def draw_label_contours(self, page, rects: list):
        for i, r in enumerate(rects):
            x, y, w, h = r
            center_x = x + w // 2
            center_y = y + h // 2

            cv2.putText(
                page, str(i + 1),
                (center_x, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,0,255), 2)
