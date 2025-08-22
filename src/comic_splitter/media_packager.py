import io
import os
import cv2
import zipfile

from cv2.typing import MatLike
from comic_splitter.config import ZIP_NAME, DOWNLOAD_PATH


class MediaPackager:
    def __init__(self, images: list[MatLike],
                 path: str = DOWNLOAD_PATH,
                 filename: str = ZIP_NAME):
        self.images = images
        self.validate_filepath(path)
        self.download_path = os.path.join(path, filename)

    def validate_filepath(self, path: str):
        if not os.path.isdir(path):
            raise Exception(f'Invalid Path: {path}')

    def download(self):
        files = self._convert_images_to_files()
        zip_buffer = self._zip(files)
        with open(self.download_path, 'wb') as fd:
            fd.write(zip_buffer.getvalue())

    def _convert_images_to_files(
            self, ext: str = 'jpg') -> list[tuple[str, bytes]]:
        image_files = []
        for i, image in enumerate(self.images):
            encoding_status, encoded_image = cv2.imencode('.jpg', image)
            if encoding_status:
                img_bytes = encoded_image.tobytes()
                file_name = f'{i}.{ext}'
                file = (file_name, img_bytes)
                image_files.append(file)
        return image_files

    def _zip(self, files: list[tuple[str, bytes]]):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a',
                             zipfile.ZIP_DEFLATED) as zip_file:
            for filename, file_bytes in files:
                zip_file.writestr(filename, file_bytes)
        return zip_buffer
