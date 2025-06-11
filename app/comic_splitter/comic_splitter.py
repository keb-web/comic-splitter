from collections import defaultdict
import numpy as np
import cv2


class ComicSplitter:
    def __init__(self):
        pass

    def split_page(self):
        return []

    # TODO: Encapsulate to edge-detection-specific class to maintain SRP
    def get_panel_shapes(self, contours: list[cv2.typing.MatLike]):
        rects = []
        for contour in contours:
            rects.append(cv2.boundingRect(contour))
        return rects

    def get_panel_contours(self, page: np.ndarray) -> list:
        edge_page = self._preprocess_image(page)
        contours, _ = cv2.findContours(
            edge_page, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return self._approximate_contours(contours)

    def _preprocess_image(self, page: np.ndarray) -> np.ndarray:
        blur_page = cv2.GaussianBlur(page, (5, 5), 0)
        thresh_page = cv2.threshold(blur_page, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        edge_page = cv2.Canny(thresh_page, 30, 200)
        return edge_page

    def _approximate_contours(self, contours):
        approximate_contours = []
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx_poly = cv2.approxPolyDP(contour, epsilon, False)
            points = approx_poly.reshape(-1, 2)
            approximate_contours.append(points)
        return approximate_contours

    def get_indexed_panels(self, panel_rects: list[tuple]) -> list[tuple]:
        # TODO: integrate variance handling
        # only works if panels are exactly lined up by y: make it at a range
        indexed_panels = []
        panels_by_y = defaultdict(list)
        for panel in panel_rects:
            panel_height = panel[1]
            panels_by_y[panel_height].append(panel)
        for panels in panels_by_y.values():
            panels_by_x = sorted(panels, key= lambda x: x[0])
            for x_panel in panels_by_x:
                indexed_panels.insert(0, x_panel)

        return indexed_panels


    # TODO: Encapsulate drawing to it's own class
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

    # def get_panel_bounds(self, page: np.ndarray):
    #     black_pixels = np.all(page == [0, 0, 0], axis=-1)
    #     y_coords, x_coords = np.where(black_pixels)
    #     min_x, max_x = np.min(x_coords), np.max(x_coords)
    #     min_y, max_y = np.min(y_coords), np.max(y_coords)
    #     return [min_x, min_y, max_x, max_y]
