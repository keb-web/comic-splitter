
from comic_splitter.page import Panel
from comic_splitter.panel_labeler import PanelLabeler


class TestPanelLabeler():

    def test_return_empty_list_given_no_panels(self):
        panels = []
        labeler = PanelLabeler()
        assert labeler.label(panels) == []

    def test_label_single_panel_given_single_panel_page(self):
        panels = [Panel(5, 5, 25, 25)]
        labeler = PanelLabeler()
        labeled_panels = labeler.label(panels)
        assert labeled_panels == labeled_panels

    # @pytest.parametrize
    def test_labeler_labels_side_by_side_panels_given_different_modes(self):
        pass

    # @pytest.parametrize
    def test_labeler_labels_stacked_panels_top_to_bottom(self):
        pass
