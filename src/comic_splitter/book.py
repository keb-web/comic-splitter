from comic_splitter.page import Page
from comic_splitter.config import MEDIA_PATH


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

    def __bool__(self):
        if self.metadata and self.pages and self.page_images:
            return True
        return False

    def to_json(self):
        author = self.metadata['author'].lower().strip()
        title = self.metadata['title'].lower().strip()
        chapter = self.metadata['chapter'].lower().strip()
        content_path = (
            MEDIA_PATH + '/' + title + '-' + author + f'/ch-{chapter}')
        return {
            'author': author,
            'title': title,
            'chapter': chapter,
            'content': content_path,
            'pages': [page.to_json(content_path) for page in self.pages],
        }
