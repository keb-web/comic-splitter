import io
import cv2
import zipfile
import pathlib

DOWNLOAD_PATH = str(pathlib.Path.home() / "Downloads")

class MediaPackager:
    def __init__(self, images: list, path: str = DOWNLOAD_PATH):
        self.download_path = path
        self.images = images

    def _zip(self):
        if self.images is None:
            return
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(
            zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            for name, file_bytes in self.images:
                zip_file.writestr(name, file_bytes)
        return zip_buffer.getvalue()

    def _convert_images_to_bytes(self):
        for i, image in enumerate(self.images):
            encoding_status, encoded_image = cv2.imencode('.jpg' , image)
            if encoding_status:
                img_bytes = encoded_image.tobytes()
                self.images[i] = (f'{i}.jpg', img_bytes)

