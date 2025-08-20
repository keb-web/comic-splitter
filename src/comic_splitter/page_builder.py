from io import BytesIO

import cv2
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
            if len(file_content) == 3:
                file_content = cv2.cvtColor(
                    file_content, cv2.COLOR_BGR2GRAY)

            file_content = cv2.copyMakeBorder(file_content,
                                              5, 5, 5, 5,
                                              cv2.BORDER_CONSTANT,
                                              value=(255, 255, 255))
            sd = SectionDetector(file_content)
            sections = sd.detect_page_sections()
            page = Page(content=file_content, sections=sections,
                        page_number=page_number)
            pages.append(page)
        return pages

    async def _decode_bytes_to_matlike_image(self, page: BytesIO) -> MatLike:
        page_contents_bytes = page.getvalue()
        page_content_arr = np.frombuffer(page_contents_bytes,
                                         dtype=np.uint8)
        page_content_matlike = cv2.imdecode(
            page_content_arr, cv2.IMREAD_GRAYSCALE)
        return page_content_matlike
