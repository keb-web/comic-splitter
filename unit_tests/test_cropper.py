import numpy as np
from comic_splitter.cropper import ImageCropper
from comic_splitter.page import Panel
from comic_splitter.page_section import PageSection
from .page_utils import PageUtils

util = PageUtils()


class TestCropper:
    def setup_method(self):
        self.page = util.generate_page(page_height=300, page_width=300)
        self.cropper = ImageCropper()

    def test_crop_image_with_no_panels_returns_original_image(self):
        indexed_panels = []
        assert self.cropper.crop(np.ndarray((0, 0)), indexed_panels) == []

    def test_crop_multiple_panels(self):
        crop_queue = [Panel(0, 0, 50, 50), Panel(100, 100, 50, 50)]
        result = self.cropper.crop(self.page, crop_queue)
        assert len(result) == 2
        assert result[0].shape == (50, 50)
        assert result[1].shape == (50, 50)

    def test_crop_section_with_page_sections(self):
        sections = [
            PageSection((10, 20), (40, 20), (10, 60), (40, 60)),
            PageSection((50, 60), (120, 60), (50, 140), (120, 140))
        ]
        result = self.cropper._crop_section(self.page, sections)
        assert len(result) == 2
        assert result[0].shape == (40, 30)
        assert result[1].shape == (80, 70)
