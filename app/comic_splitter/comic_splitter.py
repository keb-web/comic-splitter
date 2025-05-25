import numpy as np

white_pixel = np.array([255, 255, 255])

class ComicSplitter:
    def __init__(self):
        pass

    def split_page(self, page):
        return []

    def determine_panel_bounds(self, page: np.ndarray):
        height, width, channels = page.shape
        min_x, min_y = width, height
        max_x, max_y = 0, 0

        for y in range(height):
            for x in range(width):
                if np.array_equal(page[y, x], [0, 0, 0]):
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        print(f"Top-left: ({min_x}, {min_y})")
        print(f"Bottom-right: ({max_x}, {max_y})")

        return [min_x, min_y, max_x, max_y]
