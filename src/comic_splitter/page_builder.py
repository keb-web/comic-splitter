from io import BytesIO
import os

import cv2
from cv2.mat_wrapper import Mat
import numpy as np
from cv2.typing import MatLike

from comic_splitter.book import Page
from comic_splitter.section_detector import SectionDetector


class PageBuilder:
    def __init__(self, files: list[BytesIO]):
        self.files = files

    async def generate_pages(self) -> list[Page]:
        pages = []
        for page_number, file in enumerate(self.files):
            file_content = await self._decode_bytes_to_matlike_image(file)

            # we are preprocessing the image
            if len(file_content) == 3:
                file_content = cv2.cvtColor(
                    file_content, cv2.COLOR_BGR2GRAY)
            # TODO: make white if white background, make black otherwise
            white = (255, 255, 255)
            file_content = cv2.copyMakeBorder(file_content,
                                              5, 5, 5, 5,
                                              cv2.BORDER_CONSTANT,
                                              value=white)
            processed_file_content = self._preprocess_image(file_content)

            # NOTE: REFACTOR: maintain SRI by detecting only in cs class?
            sd = SectionDetector(processed_file_content)
            sections = sd.detect_page_sections()
            page = Page(content=file_content,
                        processed_content=processed_file_content,
                        sections=sections, page_number=page_number)
            pages.append(page)
        return pages

    async def _decode_bytes_to_matlike_image(self, page: BytesIO) -> MatLike:
        page_contents_bytes = page.getvalue()
        page_content_arr = np.frombuffer(page_contents_bytes,
                                         dtype=np.uint8)
        page_content_matlike = cv2.imdecode(
            page_content_arr, cv2.IMREAD_GRAYSCALE)
        if page_content_matlike is None:
            return Mat([])
        return page_content_matlike

    def _preprocess_image(self, processed_page: MatLike) -> MatLike:
        processed_page = cv2.GaussianBlur(processed_page, (5, 5), 0)
        processed_page = cv2.threshold(processed_page, 0, 255,
                                       cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        processed_page = cv2.Canny(processed_page, 30, 200)
        processed_page = cv2.bitwise_not(processed_page)
        return processed_page
