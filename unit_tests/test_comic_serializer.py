from comic_splitter.book import Book
from comic_splitter.database import ComicSerializer


class TestComicSerializer:

    def test_serializer_returns_nothing_given_empty_book(self):
        serializer = ComicSerializer()
        book = Book(metadata={})
        assert serializer.to_json(book) == {}

    # def test_serializer_returns_book_data_as_json(self):
    #     serializer = ComicSerializer
    #     dummy_metadata = {
    #         'author': 'dummy-author',
    #         'title': "dummy-comic",
    #         'chapter': "1"
    #     }
    #     book = Book(dummy_metadata)
    #     book_json = serializer.to_json(book)
    #     assert book_json == {
    #         'author': 'keb',
    #         'title': "keb's comic",
    #         'chapter': '1',
    #         'contentpath': '/assets/author/kebs-comic/ch1/'
    #     }
