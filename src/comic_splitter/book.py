from comic_splitter.page import Page


class Book:
    def __init__(self, metadata: dict = {}):
        self.metadata = metadata
        self.pages = []
        self.page_images = []
        self.filetype = ''

    def get_pages(self) -> list[Page]:
        return self.pages

    def add_page(self, page: Page):
        self.pages.append(page)

    def set_filetype(self, filetype: str):
        filetype = filetype.lower().strip()
        self.filetype = filetype

    def set_metadata(self, metadata: dict):
        for k, v in metadata.items():
            print(k, v)
            if isinstance(v, str):
                self.metadata[k] = v.lower().strip()
            else:
                self.metadata[k] = v

    def set_pages(self, pages: list[Page]):
        self.pages = pages

    def __bool__(self):
        if self.metadata and self.pages and self.page_images:
            return True
        return False

    def to_json(self):
        return {
            'author': self.metadata.get('author'),
            'title': self.metadata.get('title'),
            'entry_number': self.metadata.get('entry_number'),
            'filetype': self.filetype,
            'pages': [page.to_json() for page in self.pages],
        }
