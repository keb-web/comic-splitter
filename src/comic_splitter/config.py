import datetime
import pathlib

VALID_FILE_TYPES = ['jpg', 'png', 'jpeg']
ZIP_NAME = f'comic-split-{
                datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.zip'
DOWNLOAD_PATH = str(pathlib.Path.home() / "Downloads")
