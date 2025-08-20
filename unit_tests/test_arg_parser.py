from argparse import Namespace

from fastapi import UploadFile

from comic_splitter.argument_parser import (get_options_from_args)


class TestArgParser:

    def test_arg_to_option_dict_conversion(self):
        dummy_file_path = '/asset/test_image.jpg'
        args = Namespace(image=dummy_file_path,
                         cropmode='crop', margins=1,
                         label=True, blank=True)
        options = get_options_from_args(args)
        assert options == {'mode': 'crop', 'margins': 1,
                           'label': True, 'blank': True}
