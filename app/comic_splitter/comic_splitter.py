import numpy as np

white_pixel = np.array([255, 255, 255])

class ComicSplitter:
    def __init__(self):
        pass

    def split_page(self, page):
        return []

    def determine_panel_bounds(self, page: np.ndarray):
        height, width, channels = page.shape
        black_pixels = np.all(page == [0, 0, 0], axis=-1)
        y_coords, x_coords = np.where(black_pixels)
        min_x, max_x = np.min(x_coords), np.max(x_coords)
        min_y, max_y = np.min(y_coords), np.max(y_coords)
        return [min_x, min_y, max_x, max_y]
