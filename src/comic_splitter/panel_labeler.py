
from typing import Literal
from comic_splitter.page import Panel


class PanelLabeler():
    def __init__(self, direction: Literal['RTL', 'LTR'] = 'RTL'):
        self.reading_direction = direction

    def label(self, panels: list[Panel]):
        if panels == []:
            return panels
        pass
