import json

from comic_splitter.book import Book


class ComicSerializer:

    def to_json(self, book: Book):
        if not book:
            return {}
        return json.dumps(book.__dict__)
    pass
