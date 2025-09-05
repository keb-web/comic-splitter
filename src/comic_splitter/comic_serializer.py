import json
from comic_splitter.book import Book


class ComicSerializer:
    @staticmethod
    def to_json(book: Book):
        if not book:
            return {}
        book_data = book.to_json()
        return json.dumps(book_data)
