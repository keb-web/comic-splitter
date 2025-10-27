from io import BytesIO
import pytest

from fastapi import UploadFile
from comic_splitter.file_adapter import FileAdapter


class TestFileAdapter:

    def test_adapter_does_nothing_if_given_correct_type(self):
        dummy_file_data = BytesIO(b'dummy data')
        adapter = FileAdapter()
        assert adapter.source_to_binary_io(dummy_file_data) == dummy_file_data

    def test_adapter_returns_bytesio_given_uploadfile(self):
        dummy_file_data = BytesIO(b'dummy data')
        dummy_uploadfile = UploadFile(file=dummy_file_data)
        adapter = FileAdapter()
        uploadfile_as_bytesio = adapter.source_to_binary_io(dummy_uploadfile)
        assert isinstance(uploadfile_as_bytesio, BytesIO)

    def test_adapter_returns_bytesio_given_local_filepath(self, tmp_path):
        file = tmp_path / "image.jpg"
        file.write_bytes(b"dummy data")
        adapter = FileAdapter()
        result = adapter.source_to_binary_io(str(file))
        assert isinstance(result, BytesIO)
        assert result.getvalue() == b"dummy data"

    def test_adapter_raises_error_given_invalid_filepath(self):
        adapter = FileAdapter()
        with pytest.raises(FileNotFoundError):
            adapter.source_to_binary_io("/path/that/does/not/exist.jpg")

    def test_adapter_raises_error_given_invalid_type(self):
        adapter = FileAdapter()
        unsupported_input = 123456
        with pytest.raises(TypeError):
            adapter.source_to_binary_io(unsupported_input)
