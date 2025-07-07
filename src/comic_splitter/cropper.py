
import numpy as np

class ImageCropper:
    def crop(self, image: np.ndarray,
             crop_queue: list[tuple]) -> list:
        cropped_images = []
        for crop_values in crop_queue:
            x, y, width, height = crop_values
            cropped_image = image[y:y+height, x:x+width]
            cropped_images.append(cropped_image)
        return cropped_images
