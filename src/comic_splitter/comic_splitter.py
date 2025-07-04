from fastapi import File, UploadFile

from comic_splitter.cropper import ImageCropper
from comic_splitter.etcher import Etcher
from comic_splitter.media_packager import MediaPackager
from comic_splitter.panel_detector import PanelDetector

class ComicSplitter:
    def __init__(self, files: list[UploadFile]):
        self.files = files
        self.cropper = ImageCropper()
        self.etcher = Etcher()

    # returns list[File]
    async def split(self) -> list:
        # basic implementation
        # read in File (bytes) (asyunc task)
        return [await self.files[0].read()]

        # make this cpu-bound blocking
        # run each file byte through panel detection

        # create new files with etcher or crop

        # package zip

        # return list of new files (bytes) and cache zip (optional)

        # zip should be exposed to a get request for later retrieval
        return []
 
    def split_page(self):
        return []
