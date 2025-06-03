from collections import defaultdict
import os
import numpy as np
import cv2

white_pixel = np.array([255, 255, 255])

class ComicSplitter:
    def __init__(self):
        pass

    def split_page(self):
        return []

    def preprocessing(self, page: np.ndarray) -> tuple:
        blur_page = cv2.GaussianBlur(page, (5, 5), 0)
        # thresh_page = cv2.threshold(blur_page, 0, 255,
        #                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        thresh_page = cv2.adaptiveThreshold(blur_page, 255, 
                                cv2.ADAPTIVE_THRESH_MEAN_C, 
                                cv2.THRESH_BINARY, 
                                blockSize=11, C=2)
        edge_page = cv2.Canny(thresh_page, 30, 200)

        return blur_page, thresh_page, edge_page


    def get_panel_contours(self, page: np.ndarray) -> list: 
        _, _, edge_page = self.preprocessing(page)

        contours, _ = cv2.findContours(
            edge_page, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        approx_contours = []
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx_poly = cv2.approxPolyDP(contour, epsilon, False)
            approx_contours.append(approx_poly)

        return approx_contours

    # TODO: Encapsulate drawing to it's own class
    def draw_contour(self, page: np.ndarray, contours: list, labels: bool):
        height, width = page.shape
        blank_image = np.ones((height, width, 3), np.uint8)
        cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
        if labels:
            self.label_contours(blank_image, contours)
        return blank_image

    def label_contours(self, page, contours: list):
        labels = defaultdict(list)

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
            
            labels[panel_number] = contour
            panel_number-=1
        return labels

    def get_panel_bounds(self, page: np.ndarray):
        black_pixels = np.all(page == [0, 0, 0], axis=-1)
        y_coords, x_coords = np.where(black_pixels)
        min_x, max_x = np.min(x_coords), np.max(x_coords)
        min_y, max_y = np.min(y_coords), np.max(y_coords)
        return [min_x, min_y, max_x, max_y]
