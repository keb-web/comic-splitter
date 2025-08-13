import argparse
import os
from typing import BinaryIO

from fastapi import UploadFile


VALID_FILE_TYPES = ['jpg', 'png', 'jpeg']

def file_path(path: str) -> str:
    if os.path.isfile(path):
        return path
    raise argparse.ArgumentTypeError(f"File does not exist: {path}")

def dir_path(path: str) -> str:
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"Directory does not exist: {path}")

def mode(mode: str):
    if mode in ['etch', 'crop']:
        return mode
    raise argparse.ArgumentTypeError("Mode must be 'etch' or 'crop'")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Comic Panel Detection using Computer Vision')

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i", "--image", type=file_path,
        help='Path to image file')
    input_group.add_argument(
        "-d", "--dir", type=dir_path,
        help='Path to images directory')

    parser.add_argument(
        "-c", "--cropmode", type=mode, default='crop',
        help="Specify 'etch' or 'crop' mode")
    parser.add_argument(
        "-m", "--margins", type=int, default=1,
        help='Specify margin size (pixels)')
    parser.add_argument(
        '-l', '--label', action=argparse.BooleanOptionalAction,
        help='Label panel numbers')
    parser.add_argument(
        '-b', '--blank', action=argparse.BooleanOptionalAction,
        help='fill detected contours')

    args = parser.parse_args()
    return args

def _check_valid_file_extension(file_paths: list[str]):
    exts = [fp.rsplit('.', -1)[-1].lower() for fp in file_paths]
    for i, file_extension in enumerate(exts):
        if file_extension not in VALID_FILE_TYPES:
            raise argparse.ArgumentTypeError(
                f"Error: incompatible file: {file_paths[i]}")
    return file_paths

def get_options_from_args(args: argparse.Namespace) -> dict:
    options = {}
    options['mode'] = args.cropmode
    options['margins'] = args.margins
    options['label'] = args.label
    options['blank'] = args.blank
    return options

# TODO: 
# this should eventually just make API calls instead of manually
# creating upload files
def get_upload_files_from_paths(paths: list[str]) -> list[UploadFile]:
    upload_files = []
    for path in paths:
        with open(path, "rb") as f:
            file_content: BinaryIO = f
            upload_file = UploadFile(file=file_content)
            upload_files.append(upload_file)
    return upload_files

if __name__ == '__main__':
    args = parse_arguments()
    file_paths = []
    if args.image:
        file_paths = _check_valid_file_extension([args.image])
    if args.dir:
        entries = os.listdir(args.dir)
        file_paths = []
        for entry in entries:
            full_path = os.path.join(args.dir, entry)
            if os.path.isfile(full_path):
                file_paths.append(full_path)
        file_paths = _check_valid_file_extension(file_paths)
    options = get_options_from_args(args)
    upload_files = get_upload_files_from_paths(file_paths)
    # cs = ComicSplitter(upload_files, options)

