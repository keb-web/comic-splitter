import numpy as np
import cv2
import os

class PageUtils:

    def generate_page(self, rectangle_coords: list[tuple[tuple, tuple]],
                      page_height: int = 3035, page_width: int = 2150,
                      color: tuple = (0, 0, 0), thickness: int = 5):

        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for coord in rectangle_coords:
            start_xy, end_xy = coord[0], coord[1]
            cv2.rectangle(page, start_xy, end_xy,
                          color=color, thickness=thickness)
        return page

class VisionUtils:
    def draw_labels(self, img, contours, splitter):
        height, width = img.shape
        empty_image = np.zeros((height, width), dtype=np.int8)
        labeled_image = splitter.draw_contour(empty_image, contours, True)
        self.save_image(labeled_image)

    def view_image(self, img: np.ndarray):
        cv2.imshow('test_window', img)
        cv2.waitKey(0)
    
    def save_image(self, img: np.ndarray,
                   filename: str = 'debug_output'):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        save_path = os.path.join(project_root, f'{filename}.jpg')
        cv2.imwrite(save_path, img)
