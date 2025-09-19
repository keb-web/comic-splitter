from cv2.typing import MatLike
import numpy as np

from comic_splitter.page import Panel
from comic_splitter.page_section import PageSection


class ImageCropper:

    def crop(self, image: np.ndarray,
             crop_queue: list[Panel]) -> list[MatLike]:

        cropped_images = []
        for panel in crop_queue:
            cropped_image = image[panel.y: panel.y + panel.height,
                                  panel.x: panel.x + panel.width]
            cropped_images.append(cropped_image)
        return cropped_images

    def crop_panel(self, image: np.ndarray, panel: Panel) -> MatLike:
        cropped_image = image[panel.y: panel.y + panel.height,
                              panel.x: panel.x + panel.width]
        return cropped_image

    def _crop_section(self, image: np.ndarray,
                      section_queue: list[PageSection]) -> list:
        cropped_images = []
        for section in section_queue:
            x, y = section.x, section.y
            width, height = section.width, section.height
            cropped_image = image[y:y+height, x:x+width]
            cropped_images.append(cropped_image)

        return cropped_images
