from cv2.typing import MatLike
import numpy as np
import io
import zipfile
from unittest.mock import MagicMock, patch, mock_open
from comic_splitter.media_packager import MediaPackager

# parent of children that will contain different types of media packagers


class TestMediaPackager:

    # def test_packager_returns_nothing_with_no_input(self, mock_imwrite):
    #     dummy_path = './dummy/path'
    #     dummy_images = []
    #
    #     packager = MediaPackager(dummy_images, dummy_path)
    #     packager._zip(None)
    #
    #     mock_imwrite.assert_not_called()

    def test_packager_converts_images_to_bytes(self):
        dummy_images: list[MatLike] = [np.ones((1, 1), dtype=np.uint8),
                                       np.ones((1, 1), dtype=np.uint8)]
        packager = MediaPackager(dummy_images)
        images_as_bytes = packager._convert_images_to_files()
        for i, (filename, file_bytes) in enumerate(images_as_bytes):
            assert filename == f'{i}.jpg'
            assert isinstance(file_bytes, bytes)

    def test_packager_zip_function(self):
        dummy_images: list[MatLike] = [np.ones((1, 1), dtype=np.uint8),
                                       np.ones((1, 1), dtype=np.uint8)]
        dummy_image_bytes = [('1.jpg', b'fakebytes1'),
                             ('2.jpg', b'fakebytes2')]
        packager = MediaPackager(dummy_images)
        zip_buffer = packager._zip(dummy_image_bytes)
        assert zip_buffer is not None
        # zip_buffer = io.BytesIO(zip_buffer.getvalue())
        with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
            namelist = zip_file.namelist()
            assert '1.jpg' in namelist
            assert '2.jpg' in namelist
            assert zip_file.read('1.jpg') == b'fakebytes1'
            assert zip_file.read('2.jpg') == b'fakebytes2'

    def test_packager_downloads_zip_buffer(self):
        mock_bytes_io = MagicMock(spec=io.BytesIO)
        packager = MediaPackager([])
        with patch.object(packager, '_zip', return_value=mock_bytes_io), \
             patch('builtins.open', mock_open()) as mock_file:
            packager.download()
            mock_file.assert_called_once_with(
                f'{packager.download_path}', 'wb')
            mock_file().write.assert_called_once_with(mock_bytes_io.getvalue())
