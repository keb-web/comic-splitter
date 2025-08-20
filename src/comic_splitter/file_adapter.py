from io import BytesIO
from typing import Any, List

from starlette.datastructures import UploadFile

# TODO: add filesize checker, if too large raise an error
# Make a Generator using yield to not use too much ram with large files
# make async to work concurrently with FastAPI


class FileAdapter:

    def source_to_binary_io(
            self, source: BytesIO | UploadFile | str | Any) -> BytesIO:
        if isinstance(source, BytesIO):
            return source
        elif isinstance(source, UploadFile):
            return BytesIO(source.file.read())
        elif isinstance(source, str):
            with open(source, 'rb') as file:
                return BytesIO(file.read())
        else:
            raise TypeError('Invalid FileType')

    def sources_to_binary_io(self, sources: List[Any]) -> list[BytesIO]:
        return [self.source_to_binary_io(src) for src in sources]
