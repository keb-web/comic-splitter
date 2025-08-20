class PageBuilder:
    def __init__(self, cropper: ImageCropper, panel_detector: PanelDetector):
        self.cropper = cropper
        self.panel_detector = panel_detector

    async def build_pages(self, files: list, options: dict) -> list[Page]:
        pages = []
        for page_number, file in enumerate(files):
            page_content = await self._decode_bytes_to_matlike_image(file)
            # optional preprocessing
            gray_content = cv2.cvtColor(page_content, cv2.COLOR_BGR2GRAY)
            padded_content = cv2.copyMakeBorder(gray_content, 4, 4, 4, 4,
                                                cv2.BORDER_CONSTANT, value=(255,255,255))
            sections = SectionDetector(page_content).detect_page_sections()
            page = Page(content=padded_content, sections=sections, page_number=page_number)

            # panel detection
            panels = []
            for section in page.get_sections():
                panels.extend(self.panel_detector.detect_panels(section))
            page.set_panels(panels)

            pages.append(page)
        return pages

    async def _decode_bytes_to_matlike_image(self, page) -> MatLike:
        page_contents_bytes = await page.read()
        page_content_arr = np.frombuffer(page_contents_bytes, dtype=np.uint8)
        return cv2.imdecode(page_content_arr, cv2.IMREAD_GRAYSCALE)
