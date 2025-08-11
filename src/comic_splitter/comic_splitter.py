import cv2
import numpy as np
from cv2.typing import MatLike
from fastapi import UploadFile

from comic_splitter.book import Book, Page
from comic_splitter.cropper import ImageCropper
from comic_splitter.etcher import Etcher
from comic_splitter.media_packager import MediaPackager
from comic_splitter.panel_detector import PanelDetector
from comic_splitter.section_detector import SectionDetector

# BUG:
# apply options before cropping/etching
#   (options, except for margins, should only work on etch)
# margins don't work as expected in some cases


class ComicSplitter:

    def __init__(self, files: list[UploadFile], options: dict):
        self.files = files
        self.options = options
        self.book = Book()
        self.cropper = ImageCropper()
        self.etcher = Etcher()
        self.panel_detector = PanelDetector(margins=options['margins'])

    async def split(self) -> list:
        await self._extract_panel_pages()
        panel_imgs = self.generate_panel_images(
            self.options['mode'], self.book.get_pages())
        return self.encode_panels_to_bytes(panel_imgs)

    async def _extract_panel_pages(self):
        await self._generate_pages()
        await self._detect_page_panels()

    async def _generate_pages(self):
        for page_number, file in enumerate(self.files):
            file_content = await self._decode_bytes_to_matlike_image(file)
            gray_file_content = cv2.cvtColor(file_content, cv2.COLOR_BGR2GRAY)
            padded_file_content = cv2.copyMakeBorder(gray_file_content,
                                                     4, 4, 4, 4,
                                                     cv2.BORDER_CONSTANT,
                                                     value=(255, 255, 255))
            sd = SectionDetector(file_content)
            sections = sd.detect_page_sections()
            page = Page(content=padded_file_content, sections=sections,
                        page_number=page_number)
            self.book.add_page(page)

    async def _detect_page_panels(self):
        for page in self.book.get_pages():
            panels = []
            for section in page.get_sections():
                detected_panels = self.panel_detector.detect_panels(section)
                panels.extend(detected_panels)
            page.set_panels(panels)

    async def _decode_bytes_to_matlike_image(self, page) -> MatLike:
        page_contents_bytes = await page.read()
        page_content_arr = np.frombuffer(page_contents_bytes,
                                         dtype=np.uint8)
        page_content_matlike = cv2.imdecode(
            page_content_arr, cv2.IMREAD_GRAYSCALE)
        return page_content_matlike

    def generate_panel_images(self, mode, pages: list[Page]) -> list[MatLike]:
        panel_imgs = []
        if mode == 'crop':
            for page in pages:
                # panel_imgs.extend(
                #     self.cropper.crop(page.content, page.panels)
                # )
                # print(page.get_sections())
                # panel_imgs.extend(
                #     self.cropper._crop_section(page.get_content(),
                #                                page.get_sections())
                # )
                panel_imgs.extend(page.get_sections())
        elif mode == 'etch':
            for page in pages:

                panel_imgs.append(
                    self.etcher.etch(page.content, page.panels,
                                     label=self.options['label'],
                                     blank=self.options['blank'])
                )

        if panel_imgs != []:
            print(type(panel_imgs[0]))

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
