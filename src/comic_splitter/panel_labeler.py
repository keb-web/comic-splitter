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
        self.direction: Literal['RTL', 'LTR'] = direction

    def label(self, panels: list[Panel]):
        if panels == []:
            return panels
        starting_panel = self._get_starting_panel(panels)
        distance_log = self._get_relative_distances(panels, starting_panel)
        distances = [dist for dist in distance_log.keys()]
        distances.sort()
        for i, dist in enumerate(distances):
            distance_log[dist].set_idx(self.direction, i+1)

    def _get_starting_panel(self, panels: list[Panel]) -> Panel:
        starting_panel = Panel(-1, -1, 0, 0)
        if self.direction == 'RTL':
            starting_panel = max(panels,
                                 key=lambda panel: (panel.x, -panel.y))
        if self.direction == 'LTR':
            starting_panel = max(panels,
                                 key=lambda panel: (-panel.x, -panel.y))
        return starting_panel

    def _get_relative_distances(self, panels: list[Panel],
                                starting_panel: Panel) -> dict[float, Panel]:
        distance_log = {}
        for panel in panels:
            rel_dist = self._distance(panel.centroid, starting_panel.centroid)
            distance_log[rel_dist] = panel
        return distance_log

    def _distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
