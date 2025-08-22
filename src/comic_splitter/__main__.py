import asyncio
from cv2.typing import MatLike

from comic_splitter.argument_parser import ArgumentParser
from comic_splitter.media_packager import MediaPackager
from comic_splitter.comic_splitter import ComicSplitter


def get_args():
    parser = ArgumentParser()
    parser.parse_arguments()
    options = parser.get_options()
    sources = parser.get_binary_sources()
    return options, sources


async def split_sources(sources, options) -> list[MatLike]:
    comic_splitter = ComicSplitter(sources, options)
    return await comic_splitter.split()


def package(images: list[MatLike]):
    packager = MediaPackager(images=images)
    packager.download()


def main():
    options, sources = get_args()
    split_file_data = asyncio.run(
        split_sources(sources=sources, options=options))
    package(split_file_data)


main()
