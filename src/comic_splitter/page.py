import json
from cv2.typing import MatLike

from comic_splitter.page_section import PageSection
from comic_splitter.panel import Panel


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
        self.panels = panels

    def add_panel(self, panel: Panel) -> None:
        self.panels.append(panel)

    def extend_panels(self, panels: list[Panel]) -> None:
        self.panels.extend(panels)

    def to_json(self, content_path: str):
        return {
            'page_number': self.page_number,
            'content': content_path + f'/pg-{self.page_number}',
            'panels': [panel.__dict__ for panel in self.panels]
        }
