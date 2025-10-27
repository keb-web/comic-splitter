from dataclasses import dataclass
import os
from io import BytesIO

import cv2
import matplotlib.pyplot as plt
import numpy as np
from cv2.typing import MatLike
from starlette.datastructures import UploadFile

from comic_splitter.page_section import PageSection

# TODO: add converstion of bytes to UploadFile Type (found in `test_api.py`)


@dataclass
class RectUtil:
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        self.area = self.width * self.height
        self.tl = (self.x, self.y)
        self.tr = (self.x + self.width, self.y)
        self.bl = (self.x, self.y + self.height)
        self.br = (self.x + self.width, self.y + self.height)
        self.contour = (self.x, self.y, self.width, self.height)
        self.centroid = self._centroid((self.x, self.y),
                                       (self.x + self.width,
                                        self.y+self.height))

    def _centroid(self, top_left, bottom_right) -> tuple[int, int]:
        x1, y1 = top_left
        x2, y2 = bottom_right
        return ((x1+x2)/2, (y1+y2)/2)


class PageUtils:
    def generate_file_form_data(self, rectangle_coords: list[tuple] = [],
                                page_height: int = 3035,
                                page_width: int = 2150,
                                color: tuple = (0, 0, 0),
                                thickness: int = 5):
        page = self.generate_page(rectangle_coords=rectangle_coords,
                                  page_height=page_height,
                                  page_width=page_width, color=color,
                                  thickness=thickness)

        _, encoded_img = cv2.imencode('.png', page)
        fake_image = BytesIO(encoded_img.tobytes())
        fake_upload_image = (
            "files", ("FakeFile.png", fake_image, "image/png"))
        return fake_upload_image

    def generate_upload_file(self, rectangle_coords: list[tuple] = [],
                             page_height: int = 3035, page_width: int = 2150,
                             color: tuple = (0, 0, 0), thickness: int = 5):

        page = self.generate_page(rectangle_coords=rectangle_coords,
                                  page_height=page_height,
                                  page_width=page_width, color=color,
                                  thickness=thickness)

        _, encoded_img = cv2.imencode('.png', page)
        fake_image = BytesIO(encoded_img.tobytes())
        return UploadFile(fake_image)

    def generate_page(self, rectangle_coords: list[tuple] = [],
                      page_height: int = 3035, page_width: int = 2150,
                      color: tuple = (0, 0, 0), thickness: int = 5):

        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for top_left, bottom_right in rectangle_coords:
            cv2.rectangle(page, top_left, bottom_right,
                          color=color, thickness=thickness)

        # for top_left, bottom_right in rectangle_coords:
        #     cv2.rectangle(page, top_left, bottom_right,
        #                   color=color, thickness=thickness)
        return page

    def preprocess_image(self, image):
        processed_page = cv2.GaussianBlur(image, (9, 9), 0)
        processed_page = cv2.threshold(processed_page, 0, 255,
                                       cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        processed_page = cv2.Canny(processed_page, 30, 200)
        processed_page = cv2.bitwise_not(processed_page)
        return processed_page

    def generate_page_from_rects(self, rectangles: list[RectUtil],
                                 page_height: int = 500,
                                 page_width: int = 300,
                                 border_color: tuple = (0, 0, 0),
                                 thickness: int = 10):

        page = np.ones((page_height, page_width), dtype=np.uint8) * 255
        for rect in rectangles:
            cv2.rectangle(page, rect.tl, rect.br,
                          color=border_color, thickness=thickness)
        # return self.preprocess_image(page)
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

    def draw_page_sections(self, img: MatLike, sections: list[PageSection]):
        if len(img.shape) < 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        for section in sections:
            red = (0, 0, 255)
            tl = section.top_left
            br = section.bottom_right
            img = cv2.rectangle(img, tl, br, red, 1)
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
