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

    def get_idx(self, dir: Literal['RTL', 'LTR'] = 'RTL'):
        if hasattr(self, 'rtl_idx') or hasattr(self, 'ltr_idx'):
            return self.rtl_idx if dir == 'RTL' else self.ltr_idx
        raise AttributeError('Panel index has not been set')

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

    def __hash__(self):
        return hash((self.x, self.y))
