
import pytest
import math
from comic_splitter.page import Panel
from comic_splitter.panel_labeler import PanelLabeler


class TestPanel():

    def test_raise_error_when_getting_missing_panel_idx(self):
        dummy_panel = Panel(0, 0, 0, 0)
        with pytest.raises(AttributeError,
                           match="Panel index has not been set"):
            dummy_panel.get_idx()


class TestPanelLabeler():

    def test_return_empty_list_given_no_panels(self):
        panels = []
        labeler = PanelLabeler()
        assert labeler.label(panels) == []

    @pytest.mark.parametrize('dir', ['RTL', 'LTR'])
    def test_label_single_panel_given_single_panel_page(self, dir):
        panels = [Panel(5, 5, 25, 25)]
        labeler = PanelLabeler(dir)
        labeler.label(panels)

        assert len(panels) == 1
        assert panels[0].get_idx(dir) == 1

    @pytest.mark.parametrize('dir, indicies',
                             [('RTL', [3, 2, 1]), ('LTR', [1, 2, 3])])
    def test_labeler_labels_side_by_side_panels(self, dir, indicies):
        left_panel = Panel(x=5, y=5, width=25, height=25)
        middle_panel = Panel(x=30, y=5, width=25, height=25)
        right_panel = Panel(x=60, y=5, width=25, height=25)
        panels = [left_panel, middle_panel, right_panel]
        labeler = PanelLabeler(dir)
        labeler.label(panels)

        assert len(panels) == 3
        sorted_indices = [p.get_idx(dir) for p in panels]
        assert sorted_indices == indicies

    @pytest.mark.parametrize('dir', ['RTL', 'LTR'])
    def test_labeler_labels_stacked_panels(self, dir):
        top_panel = Panel(x=5, y=5, width=25, height=25)
        bottom_panel = Panel(x=5, y=30, width=25, height=25)
        panels = [top_panel, bottom_panel]
        labeler = PanelLabeler(dir)
        labeler.label(panels)

        assert len(panels) == 3
        sorted_indices = [p.get_idx(dir) for p in panels]
        assert sorted_indices == [1, 2, 3]

    @pytest.mark.parametrize('dir, panel', [('RTL', (25, 25)),
                                            ('LTR', (0, 0))])
    def test_labeler_identifies_starting_panel(self, dir, panel):
        top_left_panel = Panel(x=0, y=0, width=5, height=5)
        top_right_panel = Panel(x=25, y=25, width=5, height=5)
        panels = [top_left_panel, top_right_panel]
        labeler = PanelLabeler(dir)
        starting_panel = labeler._get_starting_panel(panels)
        assert (starting_panel.x, starting_panel.y) == panel

    def distance(self, p1, p2):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def test_labeler_identifies_panel_distance(self):
        left_panel = Panel(x=5, y=5, width=25, height=25)
        middle_panel = Panel(x=30, y=5, width=25, height=25)
        right_panel = Panel(x=60, y=5, width=25, height=25)
        panels = [left_panel, middle_panel, right_panel]
        labeler = PanelLabeler()
        starting_panel = right_panel

        dist = labeler._get_relative_distances(panels=panels,
                                               starting_panel=starting_panel)

        assert dist == {
            left_panel: self.distance(left_panel, starting_panel),
            middle_panel: self.distance(middle_panel, starting_panel),
            right_panel: self.distance(right_panel, starting_panel)
        }
