from cv2.typing import MatLike
import tempfile
import numpy as np
import io
import zipfile
from unittest.mock import MagicMock, patch, mock_open
from comic_splitter.media_packager import MediaPackager


class TestMediaPackager:

    def test_packager_converts_images_to_bytes(self):
        dummy_images: list[MatLike] = [np.ones((1, 1), dtype=np.uint8),
                                       np.ones((1, 1), dtype=np.uint8)]

        with tempfile.TemporaryDirectory() as tmp_dir:
            packager = MediaPackager(dummy_images, path=tmp_dir)
        images_as_bytes = packager._convert_images_to_files()
        for i, (filename, file_bytes) in enumerate(images_as_bytes):
            assert filename == f'{i}.jpg'
            assert isinstance(file_bytes, bytes)

    def test_packager_zip_function(self):
        dummy_images: list[MatLike] = [np.ones((1, 1), dtype=np.uint8),
                                       np.ones((1, 1), dtype=np.uint8)]
        dummy_image_bytes = [('1.jpg', b'fakebytes1'),
                             ('2.jpg', b'fakebytes2')]
        with tempfile.TemporaryDirectory() as tmp_dir:
            packager = MediaPackager(dummy_images, path=tmp_dir)
        zip_buffer = packager._zip(dummy_image_bytes)
        assert zip_buffer is not None
        with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
            namelist = zip_file.namelist()
            assert '1.jpg' in namelist
            assert '2.jpg' in namelist
            assert zip_file.read('1.jpg') == b'fakebytes1'
            assert zip_file.read('2.jpg') == b'fakebytes2'

    def test_packager_downloads_zip_buffer(self):
        mock_bytes_io = MagicMock(spec=io.BytesIO)
        with tempfile.TemporaryDirectory() as tmp_dir:
            packager = MediaPackager([], path=tmp_dir)
        with patch.object(packager, '_zip', return_value=mock_bytes_io), \
             patch('builtins.open', mock_open()) as mock_file:
            packager.download()
            mock_file.assert_called_once_with(
                f'{packager.download_path}', 'wb')
            mock_file().write.assert_called_once_with(mock_bytes_io.getvalue())
