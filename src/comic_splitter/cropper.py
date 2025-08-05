
import numpy as np

from comic_splitter.book import PageSection

class ImageCropper:

    def crop(self, image: np.ndarray,
             crop_queue: list[tuple]) -> list:

        cropped_images = []
        for crop_values in crop_queue:
            x, y, width, height = crop_values
            cropped_image = image[y:y+height, x:x+width]
            cropped_images.append(cropped_image)
        return cropped_images

    # TODO: delete
    def _crop_section(self, image: np.ndarray,
             crop_queue: list) -> list:
        print(crop_queue)

        cropped_images = []
        for section in crop_queue:
            x, y = section.x_offset, section.y_offset
            width, height = section.width, section.height
            cropped_image = image[y:y+height, x:x+width]
            cropped_images.append(cropped_image)

        return cropped_images
