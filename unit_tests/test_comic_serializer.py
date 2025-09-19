import json
import unittest
from unittest.mock import MagicMock

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
                'centroid': (15.0, 20.0),
                'content': ''
            }

    def test_page_to_json(self):
        panel = Panel(x=5, y=5, width=20, height=30, rtl_idx=2, ltr_idx=1)
        page = Page(content=MagicMock(), processed_content=MagicMock(),
                    sections=[], page_number=1)
        page.set_panels([panel])
        json = page.to_json()
        assert json['page_number'] == 1
        assert len(json['panels']) == 1

    def test_serializer_returns_book_data_as_json(self):
        dummy_panel_content_1 = 'panel1'
        dummy_panel_content_2 = 'panel2'
        panel_left = Panel(x=5, y=5, width=20, height=30,
                           rtl_idx=2, ltr_idx=1)
        panel_right = Panel(x=25, y=5, width=20, height=30,
                            rtl_idx=1, ltr_idx=2)
        panel_left.content = dummy_panel_content_1
        panel_right.content = dummy_panel_content_2
        dummy_panels = [panel_left, panel_right]
        page_1 = Page(content=MagicMock(), processed_content=MagicMock(),
                      sections=[], page_number=1)
        page_1.panels = dummy_panels
        dummy_metadata = {
            'author': 'dummy-author',
            'title': "dummy-comic",
            'chapter': "1",
            'filetype': 'dummy-type'
        }
        book = Book(dummy_metadata)
        book.add_page(page_1)
        book.page_images = [MagicMock()]
        book_dict = book.to_json()

        image_type = 'dummy-type'

        expected_dict = {
                'author': 'dummy-author',
                'title': 'dummy-comic',
                'chapter': '1',
                'filetype': image_type,
                'pages': [
                    {
                        'page_number': 1,
                        'panels': [
                            {
                                'x': 5,
                                'y': 5,
                                'width': 20,
                                'height': 30,
                                'rtl_idx': 2,
                                'ltr_idx': 1,
                                'centroid': (15.0, 20.0),
                                'content': dummy_panel_content_1
                            },
                            {
                                'x': 25,
                                'y': 5,
                                'width': 20,
                                'height': 30,
                                'rtl_idx': 1,
                                'ltr_idx': 2,
                                'centroid': (35.0, 20.0),
                                'content': dummy_panel_content_2
                            }
                        ],
                    },
                ],
            }
        assert book_dict == expected_dict
        assert ComicSerializer.to_json(book) == json.dumps(expected_dict)
