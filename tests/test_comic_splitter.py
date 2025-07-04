from io import BytesIO

from fastapi import UploadFile

# from starlette.applications import StarletteUploadFile
from comic_splitter.comic_splitter import ComicSplitter
import pytest

class TestComicSplitter:

    @pytest.mark.asyncio
    async def test_split_reads_file(self):
        comic_data = BytesIO(b'dummydata')
        fake_files = [UploadFile(file=comic_data, filename='dummyfile')]
        cs = ComicSplitter(fake_files)
        read_file = await cs.split()
        print(read_file)
        assert read_file == [b'dummydata']


