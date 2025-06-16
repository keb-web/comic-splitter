import numpy as np
import cv2

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

