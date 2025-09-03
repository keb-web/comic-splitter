from dataclasses import dataclass
from typing import Literal


@dataclass
class Panel:
    x: int
    y: int
    width: int
    height: int
    rtl_idx: int = -1
    ltr_idx: int = -1

    def __post_init__(self):
        self.centroid = self._centroid()

    def get_idx(self, dir: Literal['RTL', 'LTR'] = 'RTL'):
        return self.rtl_idx if dir == 'RTL' else self.ltr_idx

    def set_idx(self, dir: Literal['RTL', 'LTR'], idx: int):
        if dir == 'RTL':
            self.rtl_idx = idx
        else:
            self.ltr_idx = idx

    def get_rect(self) -> tuple:
        return (self.x, self.y, self.width, self.height)

    def get_edge_ref(self, dir: Literal['RTL', 'LTR'] = 'RTL'):
        if dir == 'RTL':
            top_right_point = (self.x + self.width, self.y)
            return top_right_point
        else:
            top_left_point = (self.x, self.y)
            return top_left_point

    def _centroid(self):
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height
        return (x1+x2)/2, (y1+y2)/2

    def __hash__(self):
        return hash((self.x, self.y))
