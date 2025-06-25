import numpy as np
import cv2


class ComicSplitter:
    def __init__(self):
        pass

    def split_page(self):
        return []


class Etcher:
        def draw_contour(self, page: np.ndarray, contours: list, labels: bool):
            height, width = page.shape
            blank_image = np.ones((height, width, 3), np.uint8)
            cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
            if labels:
                self.draw_label_contours(blank_image, contours)
            return blank_image

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
