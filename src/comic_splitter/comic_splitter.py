from io import BytesIO

from cv2.typing import MatLike

from comic_splitter.book import Book, Page
from comic_splitter.cropper import ImageCropper
from comic_splitter.etcher import Etcher
from comic_splitter.page_builder import PageBuilder
from comic_splitter.panel_detector import PanelDetector


class ComicSplitter:

    def __init__(self, files: list[BytesIO], options: dict,
                 book=None, cropper=None, etcher=None,
                 panel_detector=None, page_builder=None):
        self.options = options
        self.book = book or Book()
        self.cropper = cropper or ImageCropper()
        self.etcher = etcher or Etcher()
        self.panel_detector = panel_detector or PanelDetector()
        self.page_builder = page_builder or PageBuilder(files)

    def get_book(self):
        return self.book

    async def split(self) -> list[MatLike]:
        self.book.metadata['filetype'] = self.options['filetype']
        await self._get_book_data_from_bytes()
        self.set_panel_images(self.options['mode'], self.book.get_pages())
        panel_imgs = self.generate_panel_images(
            self.options['mode'], self.book.get_pages())
        return panel_imgs

    async def _get_book_data_from_bytes(self):
        self.book.set_pages(await self.page_builder.generate_pages())
        await self._detect_page_panels()

    async def _detect_page_panels(self):
        for page in self.book.get_pages():
            panels = []
            sections = page.get_sections()
            processsed_section_contents = page.get_processed_section_content()
            for i in range(len(sections)):
                x, y = sections[i].x, sections[i].y
                detected_panels = self.panel_detector.detect_panels(
                    processsed_section_contents[i], x, y)
                panels.extend(detected_panels)
            page.extend_panels(panels)

            print(f'section amount: {len(sections)}')
            print(f'len panels: {len(panels)}')

    def generate_panel_images(self, mode, pages: list[Page]) -> list[MatLike]:
        panel_imgs = []
        if mode == 'crop':
            # NOTE: if we are setting panel_imgs as a sideaffect to
            #  crop_panel, we cal just call that before this function.
            #  so that all this function does is collect the needed attributes
            for page in pages:
                # NOTE: Default contour-based implementation
                panel_imgs.extend(
                    self.cropper.crop(page.get_content(), page.get_panels())
                )

                # NOTE: testing sections are properly detected
                # panel_imgs.extend(
                #     self.cropper._crop_section(
                #         page.get_content(), page.get_sections()))

        elif mode == 'etch':
            for page in pages:
                # NOTE: Default contour-based implementation
                panel_imgs.append(
                    self.etcher.etch(page=page.get_content(),
                                     panels=page.get_panels(),
                                     label=self.options['label'],
                                     blank=self.options['blank'])
                )

                # NOTE: testing sections are properly detected
                # panel_imgs.append(self.etcher._etch_section(
                #     page=page.get_content(),
                #     rectangles=page.get_sections(),
                #     label=self.options['label'],
                #     blank=self.options['blank']
                # ))
        return panel_imgs

    def set_panel_images(self, mode, pages: list[Page]):
        if mode == 'crop':
            for page in pages:
                for panel in page.get_panels():
                    cropped_image = self.cropper.crop_panel(
                        page.get_content(), panel)
                    panel.set_content(cropped_image)
