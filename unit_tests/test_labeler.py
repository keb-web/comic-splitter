
import pytest
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
        labeler = PanelLabeler()
        labeler.label(panels, dir)
        assert len(panels) == 1
        assert panels[0].get_idx(dir) == 1

    @pytest.mark.parametrize('dir, indicies',
                             [('RTL', [3, 2, 1]), ('LTR', [1, 2, 3])])
    def test_labeler_labels_side_by_side_panels(self, dir, indicies):
        left_panel = Panel(x=5, y=5, width=25, height=25)
        middle_panel = Panel(x=30, y=5, width=25, height=25)
        right_panel = Panel(x=60, y=5, width=25, height=25)
        panels = [left_panel, middle_panel, right_panel]
        labeler = PanelLabeler()
        labeler.label(panels, dir)

        assert len(panels) == 3
        sorted_indices = [p.get_idx(dir) for p in panels]
        assert sorted_indices == indicies
