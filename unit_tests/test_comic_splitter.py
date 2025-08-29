from io import BytesIO
import pytest
from unittest.mock import AsyncMock, MagicMock

from comic_splitter.comic_splitter import ComicSplitter
from unit_tests.page_utils import PageUtils

utils = PageUtils()


class TestComicSplitter:
    @pytest.mark.asyncio
    async def test_splitter_extracts_nothing_from_empty_files(self):
        dummy_options = {'margins': 0, 'mode': 'crop'}
        cs = ComicSplitter(files=[], options=dummy_options)
        assert await cs.split() == []
        assert cs.book.get_pages() == []

    @pytest.mark.parametrize('mode', ['crop', 'etch'])
    @pytest.mark.asyncio
    async def test_comic_splitter_uses_correct_mode_from_options(self, mode):
        mock_book = MagicMock()
        mock_cropper = MagicMock()
        mock_etcher = MagicMock()
        mock_detector = MagicMock()
        mock_page_builder = AsyncMock()
        mock_book.get_pages.return_value = [MagicMock()]

        mock_splitter = ComicSplitter(
            files=[BytesIO(b"dummy")],
            options={"mode": f"{mode}", 'label': None, 'blank': None},
            book=mock_book,
            cropper=mock_cropper,
            etcher=mock_etcher,
            panel_detector=mock_detector,
            page_builder=mock_page_builder
        )

        await mock_splitter.split()
        if mode == 'crop':
            mock_cropper.crop.assert_called_once()
        elif mode == 'etch':
            mock_etcher.etch.assert_called_once()
