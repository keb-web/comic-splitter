from dataclasses import dataclass, field


@dataclass
class PageSection:
    top_left: tuple
    top_right: tuple
    bottom_left: tuple
    bottom_right: tuple

    bounds: tuple = field(init=False)
    x: int = field(init=False)
    y: int = field(init=False)
    height: int = field(init=False)
    width: int = field(init=False)
    slice_x: slice = field(init=False)
    slice_y: slice = field(init=False)
    centroid: tuple[int, int] = field(init=False)

    def __post_init__(self):
        self.bounds = (self.top_left, self.top_right,
                       self.bottom_left, self.bottom_right)

        x_values = [self.top_left[0], self.top_right[0],
                    self.bottom_left[0], self.bottom_right[0]]
        y_values = [self.top_left[1], self.top_right[1],
                    self.bottom_left[1], self.bottom_right[1]]
        self.x = min(x_values)
        self.y = min(y_values)

        self.width = max(x_values) - self.x
        self.height = max(y_values) - self.y

        self.slice_x = slice(self.x, self.x + self.width)
        self.slice_y = slice(self.y, self.y + self.height)
        self.centroid = self._centroid()

    def get_slice(self):
        # np[y, x]
        return self.slice_y, self.slice_x

    def _centroid(self) -> tuple[int, int]:
        x1, y1 = self.top_left
        x2, y2 = self.bottom_right
        return ((x1+x2)/2, (y1+y2)/2)

    def __repr__(self):
        return f'{self.centroid}'
