import numpy as np
import cv2
import os

class PageUtils:

    def generate_page(self, rectangle_coords: list[tuple[tuple, tuple]],
                      page_height: int = 3035, page_width: int = 2150,
                      color: tuple = (0, 0, 0), thickness: int = 5):

        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for top_left, bottom_right in rectangle_coords:
            cv2.rectangle(page, top_left, bottom_right,
                          color=color, thickness=thickness)
        return page

    def draw_labels(self, img: np.ndarray, contours):
        # height, width = img.shape
        # empty_image = np.ones((height, width), dtype=np.int8)
        page = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        labeled_image = cv2.drawContours(
            page, contours, -1, (0, 255, 0), 3)
        self.save_image(labeled_image)
    
    def save_image(self, img: np.ndarray,
                   filename: str = 'debug_output'):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        save_path = os.path.join(project_root, f'{filename}.jpg')
        cv2.imwrite(save_path, img)

    def view_image(self, img: np.ndarray):
        cv2.imshow('test_window', img)
        cv2.waitKey(0)
