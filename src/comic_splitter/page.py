from dataclasses import dataclass, field
from cv2.typing import MatLike
from comic_splitter.page_section import PageSection


@dataclass
class Panel:
    x: int
    y: int
    width: int
    height: int
    # rtl_idx: int = field(init=False)
    # ltr_indx: int = field(init=False)

    def get_rect(self) -> tuple:
        return (self.x, self.y, self.width, self.height)


class Page:
    def __init__(self, content: MatLike, processed_content: MatLike,
                 sections: list[PageSection], page_number: int = -1):
        self.content = content
        self.processed_content = processed_content
        self.sections = sections
        self.page_number = page_number
        self.panels = []

    def get_content(self) -> MatLike:
        return self.content

    def get_sections(self) -> list[PageSection]:
        return self.sections

    def get_processed_section_content(self) -> list[MatLike]:
        content_sections = []
        for section in self.sections:
            x, y = section.x, section.y
            height, width = section.height, section.width

            # Possible bug. doing y,x for numpy
            # but refactored slice does x, y on PageSectoin

            section_content = self.processed_content[y:y+height, x:x+width]
            content_sections.append(section_content)
        return content_sections

    def get_section_contents(self) -> list[MatLike]:
        content_sections = []
        for section in self.sections:
            x, y = section.x, section.y
            height, width = section.height, section.width
            section_content = self.content[y:y+height, x:x+width]
            content_sections.append(section_content)
        return content_sections

    def get_panels(self) -> list[Panel]:
        return self.panels

    def set_panels(self, panels: list[Panel]) -> None:
        self.panels = panels  # panel coutour coordinates. TODO: encapsulate

    def add_panel(self, panel: Panel) -> None:
        self.panels.append(panel)

    def extend_panels(self, panels: list[Panel]) -> None:
        self.panels.extend(panels)
