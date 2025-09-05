import json
import unittest
from unittest.mock import MagicMock
from unittest import mock

from comic_splitter.book import Book
from comic_splitter.comic_serializer import ComicSerializer
from comic_splitter.page import Page
from comic_splitter.panel import Panel


class TestComicSerializer(unittest.TestCase):

    def test_serializer_returns_nothing_given_empty_book(self):
        book = Book(metadata={})
        assert ComicSerializer.to_json(book) == {}

    def test_panel_to_json(self):
        panel = Panel(x=5, y=5, width=20, height=30, rtl_idx=2, ltr_idx=1)
        assert panel.__dict__ == {
                'x': 5,
                'y': 5,
                'width': 20,
                'height': 30,
                'rtl_idx': 2,
                'ltr_idx': 1,
                'centroid': (15.0, 20.0)
            }

    def test_page_to_json(self):
        panel = Panel(x=5, y=5, width=20, height=30, rtl_idx=2, ltr_idx=1)
        page = Page(content=MagicMock(), processed_content=MagicMock(),
                    sections=[], page_number=1)
        page.set_panels([panel])
        json = page.to_json(content_path='media')
        assert json['page_number'] == 1
        assert json['content'] == 'media/pg-1'
        assert len(json['panels']) == 1

    @mock.patch('comic_splitter.book.MEDIA_PATH', new='/media')
    def test_serializer_returns_book_data_as_json(self):
        panel_left = Panel(x=5, y=5, width=20, height=30,
                           rtl_idx=2, ltr_idx=1)
        panel_right = Panel(x=25, y=5, width=20, height=30,
                            rtl_idx=1, ltr_idx=2)
        dummy_panels = [panel_left, panel_right]
        page_1 = Page(content=MagicMock(), processed_content=MagicMock(),
                      sections=[], page_number=1)
        page_1.panels = dummy_panels
        dummy_metadata = {
            'author': 'dummy-author',
            'title': "dummy-comic",
            'chapter': "1"
        }
        book = Book(dummy_metadata)
        book.add_page(page_1)
        book.page_images = [MagicMock()]
        book_dict = book.to_json()

        expected_dict = {
                'author': 'dummy-author',
                'title': 'dummy-comic',
                'chapter': '1',
                'content': '/media/dummy-comic-dummy-author/ch-1',
                'pages': [
                    {
                        'page_number': 1,
                        'content': '/media/dummy-comic-dummy-author/ch-1/pg-1',
                        'panels': [
                            {
                                'x': 5,
                                'y': 5,
                                'width': 20,
                                'height': 30,
                                'rtl_idx': 2,
                                'ltr_idx': 1,
                                'centroid': (15.0, 20.0)
                            },
                            {
                                'x': 25,
                                'y': 5,
                                'width': 20,
                                'height': 30,
                                'rtl_idx': 1,
                                'ltr_idx': 2,
                                'centroid': (35.0, 20.0)
                            }
                        ],
                    },
                ],
            }
        assert book_dict == expected_dict
        assert ComicSerializer.to_json(book) == json.dumps(expected_dict)
