import numpy as np
import cv2
from numpy.typing import NDArray

class Etcher:

    # TODO: allow access to flags through json body in post request
    def etch(self, page: np.ndarray, rectangles: list,
             labels: bool = False, blank: bool = False) -> NDArray:
        page = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
        height, width, _ = page.shape
        canvas = np.ones((height,width,3), np.uint8) if blank else page.copy()

        for (x, y, w, h) in rectangles:
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 255), 3)

        # if labels:
        #     self.draw_label_contours(canvas, contours)

        return canvas

    def draw_label_contours(self, page, contours: list):
        panel_number = len(contours)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2

            cv2.putText(
                page, str(panel_number),
                (center_x, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,0,255), 2)
