from comic_splitter.page import Page


class Book:
    def __init__(self, metadata: dict = {}):
        self.metadata = metadata
        self.pages = []
        self.page_images = []

    def get_pages(self) -> list[Page]:
        return self.pages

    def add_page(self, page: Page):
        self.pages.append(page)

    def set_pages(self, pages: list[Page]):
        self.pages = pages
