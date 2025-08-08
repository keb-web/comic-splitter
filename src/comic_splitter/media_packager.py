import io
import cv2
import zipfile
import pathlib

DOWNLOAD_PATH = str(pathlib.Path.home() / "Downloads")


class MediaPackager:
    def __init__(self, images: list, path: str = DOWNLOAD_PATH):
        self.images = images
        self.download_path = path

    def download(self):
        img_byt = self._convert_images_to_bytes()
        zip_buffer = self._zip(img_byt)
        if zip_buffer is None:
            return
        print(type(zip_buffer))
        with open(self.download_path, 'wb') as fd:
            fd.write(zip_buffer.getvalue())

    def _zip(self, image_bytes):
        if image_bytes is None:
            return
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a',
                             zipfile.ZIP_DEFLATED) as zip_file:
            for name, file_bytes in self.images:
                zip_file.writestr(name, file_bytes)
        return zip_buffer

    def _convert_images_to_bytes(self) -> list:
        images_as_bytes = []
        for i, image in enumerate(self.images):
            encoding_status, encoded_image = cv2.imencode('.jpg', image)
            if encoding_status:
                img_bytes = encoded_image.tobytes()
                images_as_bytes.append((f'{i}.jpg', img_bytes))
        return images_as_bytes
