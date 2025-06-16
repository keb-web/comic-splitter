import numpy as np
import pytest
import io
import zipfile
from unittest.mock import MagicMock, patch
from app.comic_splitter.media_packager import MediaPackager

# NOTE: parent of children that will contain differen types of media packagers
class TestMediaPackager:

    @patch('app.comic_splitter.media_packager.cv2.imwrite')
    def test_packager_returns_nothing_with_no_media_input(self, mock_imwrite):
        dummy_path = './dummy/path'
        dummy_images = []

        packager = MediaPackager(dummy_images, dummy_path)
        packager._zip()

        mock_imwrite.assert_not_called()

    #
    # def test_packager_uses_default_path_with_bad_path_input(self):
    #     dummy_path = './bad/path'
    #     dummy_images = 
    #

    def test_packager_converts_images_to_bytes(self):
        dummy_images = [np.ones((1, 1)), np.ones((1, 1))]
        packager = MediaPackager(dummy_images)
        packager._convert_images_to_bytes()
        for i, (filename, file_bytes) in enumerate(packager.images):
            assert filename == f'{i}.jpg'
            assert isinstance(file_bytes, bytes)

    def test_packager_zip_function(self):
        dummy_image_bytes = [('1.jpg', b'fakebytes1'),
                             ('2.jpg', b'fakebytes2')]
        packager = MediaPackager(dummy_image_bytes)
        zip_bytes = packager._zip()
        assert zip_bytes is not None
        zip_buffer = io.BytesIO(zip_bytes)
        with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
            namelist = zip_file.namelist()
            print(namelist)
            assert '1.jpg' in namelist
            assert '2.jpg' in namelist
            assert zip_file.read('1.jpg') == b'fakebytes1'
            assert zip_file.read('2.jpg') == b'fakebytes2'

    def test_packager_downloads_zip_buffer(self):
        pass

    @pytest.mark.skip(reason='rearranging images to bytes')
    @patch('app.comic_splitter.media_packager.cv2.imwrite')
    def test_packager_zips_given_image_files_to_default_path(self,
                                                             mock_imwrite):
        dummy_images = MagicMock(spec=list)
        packager = MediaPackager(dummy_images)
        default_path = packager.download_path
        packager._zip()

        mock_imwrite.assert_called_with(default_path)

