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

    def __bool__(self):
        if self.metadata and self.pages and self.page_images:
            return True
        return False

    def to_json(self):
        author = self.metadata['author'].lower().strip()
        title = self.metadata['title'].lower().strip()
        entry_number = self.metadata['entry_number'].lower().strip()
        filetype = self.metadata['filetype'].lower().strip()
        return {
            'author': author,
            'title': title,
            'entry_number': entry_number,
            'filetype': filetype,
            'pages': [page.to_json() for page in self.pages],
        }
