from comic_splitter.comic_splitter import ComicSplitter
import pytest

from .page_utils import PageUtils

utils = PageUtils()


class TestComicSplitter:

    @pytest.mark.asyncio
    async def test_splitter_extracts_nothing_from_empty_files(self):
        dummy_options = {'margins': 0}
        cs = ComicSplitter(files=[], options=dummy_options)
        await cs._extract_panel_pages()
        assert cs.book.get_pages() == []

    @pytest.mark.asyncio
    async def test_generate_panel_images_with_no_image(self):
        pass

    @pytest.mark.skip(reason="WIP")
    @pytest.mark.asyncio
    async def test_generate_panel_images(self):
        top_panel = ((150, 100), (2020, 1444))
        small_bottom_panel = ((150, 1520), (10, 2911))
        files = [utils.generate_upload_file(
            rectangle_coords=[top_panel, small_bottom_panel])]
        options = {'margins': 0}
        cs = ComicSplitter(files, options)

        await cs._extract_panel_pages()

        panel_imgs = cs.generate_panel_images('crop', cs.book.get_pages())
        assert len(panel_imgs) == 2

        panel1, panel2 = panel_imgs[0],  panel_imgs[1]

        assert panel1[0][0] == (150, 100)
        assert panel2[0][0] == (150, 1520)
