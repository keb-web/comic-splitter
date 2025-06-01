import numpy as np
import cv2

white_pixel = np.array([255, 255, 255])

class ComicSplitter:
    def __init__(self):
        pass

    def split_page(self):
        return []

    def get_panel_contours(self, page: np.ndarray) -> list: 
        edge_page = cv2.Canny(page, 30, 200)
        contours, _ = cv2.findContours(
            edge_page, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        approx_contours = []
        for contour in contours:
            epsilon = 0.1 * cv2.arcLength(contour, True)
            approx_poly = cv2.approxPolyDP(contour, epsilon, False)
            approx_contours.append(approx_poly)

        return approx_contours

    def draw_contour(self, page: np.ndarray, contour):
        height, width = page.shape
        blank_image = np.ones((height, width, 3), np.uint8)
        cv2.drawContours(blank_image, contour, -1, (0, 255, 0), 3)
        return blank_image

    def get_panel_bounds(self, page: np.ndarray):
        black_pixels = np.all(page == [0, 0, 0], axis=-1)
        y_coords, x_coords = np.where(black_pixels)
        min_x, max_x = np.min(x_coords), np.max(x_coords)
        min_y, max_y = np.min(y_coords), np.max(y_coords)
        return [min_x, min_y, max_x, max_y]

