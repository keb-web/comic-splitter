from comic_splitter.book import Book, Page, PageSection
from comic_splitter.comic_splitter import ComicSplitter
import pytest

from comic_splitter.file_adapter import FileAdapter

from .page_utils import PageUtils

utils = PageUtils()


class TestComicSplitter:

    @pytest.mark.asyncio
    async def test_splitter_extracts_nothing_from_empty_files(self):
        dummy_options = {'margins': 0}
        cs = ComicSplitter(files=[], options=dummy_options)
        await cs._get_book_data_from_bytes()
        assert cs.book.get_pages() == []

    @pytest.mark.asyncio
    async def test_splitter_detects_panels_with_offset_coordinates(self):
        dummy_bounds = ((1, 1), (10, 1), (1, 5), (10, 5))
        dummy_section = PageSection(dummy_bounds, 50, 50)
        fake_page_content = utils.generate_page([((51, 51), (60, 65),)],
                                                page_height=120,
                                                page_width=120,
                                                thickness=1)
        dummy_page = Page(content=fake_page_content,
                          processed_content=fake_page_content,
                          sections=[dummy_section],)
        dummy_book = Book()
        dummy_book.add_page(dummy_page)

        dummy_options = {'margins': 0}
        cs = ComicSplitter(files=[], options=dummy_options)
        cs.book = dummy_book

        await cs._detect_page_panels()
        x, y, _, _ = cs.book.pages[0].panels[0]
        assert x >= 50 and y >= 50

    @pytest.mark.skip(reason="testing smaller components first")
    @pytest.mark.asyncio
    async def test_split(self):
        top_panel = ((150, 100), (2020, 1444))
        small_bottom_panel = ((150, 1520), (10, 2911))
        fake_page = utils.generate_upload_file(
                    rectangle_coords=[top_panel, small_bottom_panel])
        adapter = FileAdapter()
        file_data = adapter.source_to_binary_io(fake_page)
        files = [file_data]
        options = {'margins': 0, 'mode': 'crop'}
        cs = ComicSplitter(files, options)
        panels = await cs.split()
        assert len(panels) == 2

        # TODO: split this up into individual unittest
        # await cs._get_book_data_from_bytes()
        # pages = cs.book.get_pages()
        # assert len(pages) == 1
        # sections = pages[0].get_sections()
        # assert len(sections) == 2
        #
        # panel_imgs = cs.generate_panel_images('crop', cs.book.get_pages())
        # assert len(panel_imgs) == 2
        #
        # panel1, panel2 = panel_imgs[0],  panel_imgs[1]
        #
        # assert panel1[0][0] == (150, 100)
        # assert panel2[0][0] == (150, 1520)
