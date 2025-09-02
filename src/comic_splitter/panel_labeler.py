
from typing import Literal
from comic_splitter.page import Panel


class PanelLabeler():

    def label(self, panels: list[Panel],
              direction: Literal['RTL', 'LTR'] = 'RTL'):
        if panels == []:
            return panels

        order = True if direction == 'RTL' else False
        panels_by_x = sorted(panels, key=lambda panel: panel.x, reverse=order)
        for i, panel in enumerate(panels_by_x):
            panel.set_idx(direction, i+1)
