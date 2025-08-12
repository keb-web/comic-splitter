import numpy as np
import pytest
from comic_splitter.cropper import ImageCropper
from .page_utils import PageUtils

class TestCropper:

    def test_crop_image_with_no_panels_returns_original_image(self):
        indexed_panels = []
        cropper = ImageCropper()
        assert cropper.crop(np.ndarray((0, 0)), indexed_panels) == []

    @pytest.mark.skip(reason='fix later')
    def test_crop_image_with_one_panel_returns_correct_image_cropped(self):
        util = PageUtils()
        dummy_page = util.generate_page(
            rectangle_coords=[((50, 50), (250, 250))],
            page_height=300, page_width=30)
        dummy_indexed_panels = [(50, 50, 200, 200)]
        cropper = ImageCropper()
        new_pages = cropper.crop(dummy_page, dummy_indexed_panels)
        assert len(new_pages) == 1
        assert new_pages[0].shape == (200, 200)
        assert type(new_pages[0]) is np.ndarray
