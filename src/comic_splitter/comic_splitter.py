from typing import Literal
import cv2
from cv2.typing import MatLike
from fastapi import UploadFile
import numpy as np
from numpy.typing import NDArray

from comic_splitter.cropper import ImageCropper
from comic_splitter.etcher import Etcher
from comic_splitter.media_packager import MediaPackager
from comic_splitter.panel_detector import PanelDetector

# BUG: 
# apply options before cropping/etching 
#   (options, except for margins, should only work on etch)
# margins don't work as expected in some cases

class ComicSplitter:
    def __init__(self, files: list[UploadFile], options: dict):
        self.files = files
        self.options = options
        self.cropper = ImageCropper()
        self.etcher = Etcher()
        self.detector = PanelDetector(margins=options['margins'])

    async def split(self) -> list:
        comic_pages, page_panels = await self._extract_images_and_panels()
        panel_imgs = self.generate_panel_images(self.options['mode'],
                                                comic_pages, page_panels)
        return self.encode_panels_to_bytes(panel_imgs)
        # package zip (optional)
        # return list of new files (bytes) and cache zip?? (optional)
        # zip should be exposed to a get request for later retrieval
        
    async def _extract_images_and_panels(self) -> tuple:
        comic_pages, page_panels = [], []
        for file in self.files:
            file_content = await self._decode_bytes_to_matlike_image(file)
            panels = self.detector.detect_panels(file_content)
            comic_pages.append(file_content)
            page_panels.append(panels)
        return (comic_pages, page_panels)

    async def _decode_bytes_to_matlike_image(self, page) -> MatLike:
        page_contents_bytes = await page.read()
        page_content_arr = np.frombuffer(page_contents_bytes,
                                         dtype=np.uint8)
        page_content_matlike = cv2.imdecode(
            page_content_arr, cv2.IMREAD_GRAYSCALE)
        return page_content_matlike
    
    def generate_panel_images(self, mode, pages: list[NDArray], panels: list):
        panel_imgs = []
        if mode == 'crop':
            for i in range(len(self.files)):
                panel_imgs.extend(self.cropper.crop(
                    pages[i], panels[i]))
        elif mode == 'etch':
            for i in range(len(self.files)):

                # BUG: labeling got broke (horiz panels?)
                panel_imgs.append(
                    self.etcher.etch(pages[i], panels[i],
                                     label=self.options['label'],
                                     blank=self.options['blank']))
        return panel_imgs

    def encode_panels_to_bytes(self, panel_imgs, format: str = '.jpg'):
        panel_imgs_as_bytes = []
        for img_arr in panel_imgs:
            success, buf = cv2.imencode(format, img_arr)
            if not success:
                raise ValueError("Failed to encode panel image")
            img_bytes = buf.tobytes()
            panel_imgs_as_bytes.append(img_bytes)

        return panel_imgs_as_bytes
