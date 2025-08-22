import argparse
import os

from comic_splitter.config import VALID_FILE_TYPES
from comic_splitter.file_adapter import FileAdapter


class ArgumentParser:
    args: argparse.Namespace
    file_paths: list[str]
    options: dict

    def __init__(self):
        self.file_adapter: FileAdapter = FileAdapter()

    def get_arguments(self):
        if not hasattr(self, 'args'):
            self.parse_arguments()
        return self.args

    def get_file_paths(self):
        if not hasattr(self, 'file_paths'):
            self._parse_file_paths()
        return self.file_paths

    def get_options(self) -> dict:
        if not hasattr(self, 'options'):
            self._set_options()
        return self.options

    def get_binary_sources(self):
        sources = self.file_adapter.sources_to_binary_io(self.get_file_paths())
        return sources

    def file_path(self, path: str) -> str:
        if os.path.isfile(path):
            return path
        raise argparse.ArgumentTypeError(f"File does not exist: {path}")

    def dir_path(self, path: str) -> str:
        if os.path.isdir(path):
            return path
        raise argparse.ArgumentTypeError(f"Directory does not exist: {path}")

    def mode(self, mode: str):
        if mode in ['etch', 'crop']:
            return mode
        raise argparse.ArgumentTypeError("Mode must be 'etch' or 'crop'")

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description='Comic Panel Detection using Computer Vision')

        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument(
            "-i", "--image", type=self.file_path,
            help='Path to image file')
        input_group.add_argument(
            "-d", "--dir", type=self.dir_path,
            help='Path to images directory')

        parser.add_argument(
            "-c", "--cropmode", type=self.mode, default='crop',
            help="Specify 'etch' or 'crop' mode")
        parser.add_argument(
            "-m", "--margins", type=int, default=0,
            help='Specify margin size (pixels)')
        parser.add_argument(
            '-l', '--label', action=argparse.BooleanOptionalAction,
            help='Label panel numbers')
        parser.add_argument(
            '-b', '--blank', action=argparse.BooleanOptionalAction,
            help='fill detected contours')

        args = parser.parse_args()
        self.args = args

        self._parse_file_paths()
        self._set_options()

    def _parse_file_paths(self):
        file_paths = []
        if self.args.image:
            file_paths = self._check_valid_file_extension([self.args.image])
        elif self.args.dir:
            entries = os.listdir(self.args.dir)
            file_paths = []
            for entry in entries:
                full_path = os.path.join(self.args.dir, entry)
                if os.path.isfile(full_path):
                    file_paths.append(full_path)
            self._check_valid_file_extension(file_paths)
        self.file_paths = file_paths

    def _check_valid_file_extension(self, file_paths: list[str]):
        exts = [fp.rsplit('.', -1)[-1].lower() for fp in file_paths]
        for i, file_extension in enumerate(exts):
            if file_extension not in VALID_FILE_TYPES:
                raise argparse.ArgumentTypeError(
                    f"Error: incompatible file: {file_paths[i]}")
        return file_paths

    def _set_options(self):
        options = {}
        options['mode'] = self.args.cropmode
        options['margins'] = self.args.margins
        options['label'] = self.args.label
        options['blank'] = self.args.blank
        self.options = options
