import unittest
from unittest import mock
from argparse import Namespace

from comic_splitter.argument_parser import ArgumentParser


class TestArgParser(unittest.TestCase):

    def test_arg_to_option_dict_conversion(self):
        dummy_file_path = '/asset/test_image.jpg'
        args = Namespace(image=dummy_file_path,
                         cropmode='crop', margins=1,
                         label=True, blank=True)

        parser = ArgumentParser()
        parser.args = args
        options = parser.get_options()
        assert options == {'mode': 'crop', 'margins': 1,
                           'label': True, 'blank': True}

    def test_parse_file_paths_with_single_file(self):
        dummy_file_path = '/asset/test_image.jpg'
        args = Namespace(image=dummy_file_path,
                         cropmode='crop', margins=0,
                         label=True, blank=True)
        parser = ArgumentParser()
        parser.args = args
        assert parser.get_file_paths() == [dummy_file_path]

    @mock.patch('comic_splitter.argument_parser.os.path.isfile')
    @mock.patch('comic_splitter.argument_parser.os.listdir')
    def test_parse_file_paths_with_dir(self, mock_listdir, mock_isfile):
        mock_listdir.return_value = ['file1.jpg', 'file2.jpg']
        mock_isfile.return_value = True
        dummy_dir_path = '../asset/'
        dummy_file_paths = ['../asset/file1.jpg', '../asset/file2.jpg']
        args = Namespace(image=None,
                         dir=dummy_dir_path,
                         cropmode='crop', margins=0,
                         label=True, blank=True)

        parser = ArgumentParser()
        parser.args = args
        assert parser.get_file_paths() == dummy_file_paths
