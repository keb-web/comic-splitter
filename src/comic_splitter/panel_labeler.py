import math

from typing import Literal
from comic_splitter.page import Panel

'''
- create a weighted graph by distance referencing
    left edge or right edge depending on RTL or LTR
- visit top-most nearest neighbor
- requires a UPDATE operation that specifies page id and panel to update
    - each component will need their unique ID to return to JSON
'''


class PanelLabeler():
    def __init__(self, direction: Literal['RTL', 'LTR'] = 'RTL'):
        self.direction = direction

    def label(self, panels: list[Panel]):
        if panels == []:
            return panels
        starting_panel = self._get_starting_panel(panels)
        self._get_relative_distances(panels, starting_panel)

    def _get_starting_panel(self, panels: list[Panel]) -> Panel:
        starting_panel = Panel(-1, -1, 0, 0)
        if self.direction == 'RTL':
            starting_panel = max(panels, key=lambda panel: (panel.x, -panel.y))
        if self.direction == 'LTR':
            starting_panel = max(panels, key=lambda panel: (-panel.x, panel.y))
        return starting_panel

    def _get_relative_distances(self, panels: list[Panel],
                                starting_panel: Panel) -> dict[Panel, float]:
        distances = {}
        origin = (starting_panel.x, starting_panel.y)
        for panel in panels:
            distances[panel] = self._distance((panel.x, panel.y), origin)
        return distances

    def _distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
