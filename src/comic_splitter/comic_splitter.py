from io import BytesIO

import cv2
from cv2.typing import MatLike

from comic_splitter.book import Book, Page
from comic_splitter.cropper import ImageCropper
from comic_splitter.etcher import Etcher
from comic_splitter.page_builder import PageBuilder
from comic_splitter.panel_detector import PanelDetector

# BUG:
# apply options before cropping/etching
#   (options, except for margins, should only work on etch)
# margins don't work as expected in some cases


class ComicSplitter:

    def __init__(self, files: list[BytesIO], options: dict):
        self.options = options
        self.book = Book()
        self.cropper = ImageCropper()
        self.etcher = Etcher()
        self.panel_detector = PanelDetector(margins=options['margins'])
        self.page_builder = PageBuilder(files)

    async def split(self) -> list:
        await self._get_book_data_from_bytes()
        panel_imgs = self.generate_panel_images(
            self.options['mode'], self.book.get_pages())
        return self.encode_panels_to_bytes(panel_imgs)

    async def _get_book_data_from_bytes(self):
        self.book.set_pages(await self.page_builder.generate_pages())
        await self._detect_page_panels()

    async def _detect_page_panels(self):
        for page in self.book.get_pages():
            panels = []
            sections = page.get_sections()
            section_contents = page.get_section_contents()
            for i in range(len(sections)):
                x, y = sections[i].x_offset, sections[i].y_offset
                detected_panels = self.panel_detector.detect_panels(
                    section_contents[i], x, y)
                panels.extend(detected_panels)
            page.extend_panels(panels)

    def generate_panel_images(self, mode, pages: list[Page]) -> list[MatLike]:
        panel_imgs = []
        if mode == 'crop':
            for page in pages:
                # NOTE: Default implementation
                panel_imgs.extend(
                    self.cropper.crop(page.content, page.panels)
                )

                # NOTE: testing sections are properly detected
                # panel_imgs.extend(
                #     self.cropper._crop_section(
                #         page.get_content(), page.get_sections()))

        elif mode == 'etch':
            for page in pages:
                panel_imgs.append(
                    self.etcher.etch(page=page.content,
                                     rectangles=page.panels,
                                     label=self.options['label'],
                                     blank=self.options['blank'])
                )

        if panel_imgs != []:
            print(type(panel_imgs[0]))
        print(len(panel_imgs))

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
