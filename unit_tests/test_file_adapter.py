from io import BytesIO
import pytest

from fastapi import UploadFile
from comic_splitter.file_adapter import FileAdapter


class TestFileAdapter:

    def test_adapter_does_nothing_if_given_correct_type(self):
        dummy_file_data = BytesIO(b'dummy data')
        adapter = FileAdapter()
        # <class '_io.BytesIO'>
        assert adapter.source_to_binary_io(dummy_file_data) == dummy_file_data

    def test_adapter_returns_bytesio_given_uploadfile(self):
        dummy_file_data = BytesIO(b'dummy data')
        dummy_uploadfile = UploadFile(file=dummy_file_data)
        adapter = FileAdapter()
        uploadfile_as_bytesio = adapter.source_to_binary_io(dummy_uploadfile)
        assert isinstance(uploadfile_as_bytesio, BytesIO)

    @pytest.mark.skip(reason='use fake filestystem')
    def test_adapter_returns_bytesio_given_local_filepath(self):
        file_content = BytesIO(b'dummy data')
        file_path = '/dummy/file/path/image.jpg'
        adapter = FileAdapter()
        assert adapter.source_to_binary_io(file_path) == file_content

    @pytest.mark.skip(reason='use fake filestystem')
    def test_adapter_raises_error_given_invalid_filepath(self):
        pass
