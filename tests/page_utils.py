import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from numpy.typing import NDArray

class PageUtils:

    #TODO: combine both, have to refactor all tests to use ndarrays!
    def generate_page(self, rectangle_coords: list[tuple] = [],
                      page_height: int = 3035, page_width: int = 2150,
                      color: tuple = (0, 0, 0), thickness: int = 5):

        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for top_left, bottom_right  in rectangle_coords:
            cv2.rectangle(page, top_left, bottom_right,
                          color=color, thickness=thickness)

        # for top_left, bottom_right in rectangle_coords:
        #     cv2.rectangle(page, top_left, bottom_right,
        #                   color=color, thickness=thickness)
        return page

    def generate_polygonal_page(self, coords: NDArray, fill: bool = False,
                      page_height: int = 3035, page_width: int = 2150,
                      color: tuple = (0, 0, 0), thickness: int = 5):
        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        polygons = coords.reshape((-1, 3, 2))
        for poly in polygons:
            poly = poly.reshape((-1, 1, 2))  # shape (3, 1, 2) for OpenCV
            cv2.polylines(page, [poly], isClosed=True, color=color, thickness=thickness)
        return page

    def draw_labels(self, img: np.ndarray, contours):
        page = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        labeled_image = cv2.drawContours(
            page, contours, -1, (0, 255, 0), 3)
        self.save_image(labeled_image, 'labeled_output')

    def draw_lines(self, img, horiz_lines: list, vert_lines: list):
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        for y in horiz_lines:
            img = self.draw_horiz_line(img, y)
        for x in vert_lines:
            img = self.draw_vertical_line(img, x)
        return img

    def draw_vertical_line(self, img: np.ndarray, x: int):
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        height, _, _ = img.shape
        cv2.line(img, (x, 0), (x, height), (0, 0, 255), 1)
        return img

    def draw_horiz_line(self, img: np.ndarray, y: int):
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        _, width, _ = img.shape
        cv2.line(img, (0, y), (width, y), (0, 0, 255), 1)
        return img

    def show_projection(self, img: np.ndarray,
                        direction: str = 'vertical'):
        axis = 0 if direction == 'vertical' else 1
        projection = cv2.reduce(img, axis, cv2.REDUCE_SUM,
                                dtype=cv2.CV_32S).flatten()

        plt.figure(figsize=(12, 4))
        if direction == 'vertical':
            plt.title('Vertical Projection (Column-wise sum)')
            plt.xlabel('Column index')
        else:
            plt.title('Horizontal Projection (Row-wise sum)')
            plt.xlabel('Row index')
        plt.ylabel('Sum of pixel intensities')
        plt.plot(projection, color='blue')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def save_image(self, img: np.ndarray,
                   filename: str = 'debug_output'):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        save_path = os.path.join(project_root, f'{filename}.jpg')
        cv2.imwrite(save_path, img)

    def view_image(self, img: np.ndarray):
        cv2.imshow('test_window', img)
        cv2.waitKey(0)
