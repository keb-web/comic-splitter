import os
import numpy as np
import cv2


# from app.comic_splitter.comic_splitter import ComicSplitter

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

class TestComicSplitter():
    pass

