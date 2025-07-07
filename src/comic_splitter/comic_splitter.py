import cv2
from fastapi import UploadFile
import numpy as np

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
        # make file into matlike matrix for processing

        page_panels = []
        pages = []
        for page in self.files:
            page_contents_bytes = await page.read()
            page_content_arr = np.frombuffer(page_contents_bytes,
                                             dtype=np.uint8)
            page_content_matlike = cv2.imdecode(
                page_content_arr, cv2.IMREAD_GRAYSCALE)
            if page_content_matlike is None:
                raise ValueError('u fucked up!')
            else:
                pages.append(page_content_matlike)

            detector = PanelDetector(page_content_matlike)
            contours = detector.get_panel_contours()
            rects = detector.get_panel_shapes(contours)
            indexed_panels = detector.get_indexed_panels(rects)
            page_panels.append(indexed_panels)

        # create new files with etcher or crop
        # crop
        panel_imgs = []
        for i in range(len(self.files)):
            page = pages[i]
            crop_queue = page_panels[i]
            panel_imgs.extend(self.cropper.crop(page, crop_queue))
        # etcher
        # todo:
        # implement etcher

        # convert nd-array back into bytes
        panel_imgs_as_bytes = []
        print(len(panel_imgs_as_bytes))
        for img_arr in panel_imgs:
            _, buf = cv2.imencode('.jpg', img_arr)
            img_bytes = buf.tobytes()
            panel_imgs_as_bytes.append(img_bytes)

        return panel_imgs_as_bytes

        # package zip (optional)
        # return list of new files (bytes) and cache zip?? (optional)
        # zip should be exposed to a get request for later retrieval
