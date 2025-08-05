from cv2.typing import MatLike

class PageSection:

    def __init__(self, bounds, x, y):
        self.bounds = bounds
        self.top_left = bounds[0]
        self.top_right = bounds[1]
        self.bottom_left = bounds[2]
        self.bottom_right = bounds[3]
        self.height = self.bottom_left[1] - self.top_left[1] 
        self.width = self.top_right[0] - self.top_left[0]
        self.x_offset = x
        self.y_offset = y
        self.centroid = self._centroid(self.top_left, self.bottom_right)
        self.index = {}

    def _centroid(self, tl, br):
        x1, y1 = tl
        x2, y2 = br
        return ((x1+x2)/2, (y1+y2)/2)
    
    def set_index(self, index, type = 'lhs'):
        self.index[type] = index

    def __repr__(self):
        return f'{self.centroid}'

class Page:
    def __init__(
        self, content: MatLike, sections: list[PageSection],
            page_number: int = -1):
        self.content = content
        self.sections = sections
        self.page_number = page_number
        self.panels = []
        # self.cache_pages = []

    def get_content(self) -> MatLike:
        return self.content

    def get_sections(self) -> list[MatLike]:
        # if self.cache_pages != []:
        #     return self.cache_pages

        content_sections = []
        for section in self.sections:
            x, y = section.x_offset, section.y_offset
            height, width = section.height, section.width
            section_content = self.content[y:y+height, x:x+width]
            content_sections.append(section_content)

        # self.cache_pages = content_sections
        # return self.cache_pages
        return content_sections

    def set_panels(self, panels: list[tuple]):
        self.panels = panels # panel coutour coordinates

    def add_panels(self, panel: tuple):
        self.panels.append(panel)


class Book:
    def __init__(self, metadata: dict = {}):
        self.metadata = metadata
        self.pages = []
        self.page_panels = []
        self.page_images = []

    def get_pages(self) -> list[Page]:
        return self.pages

    def add_page(self, page: Page):
        self.pages.append(page)

