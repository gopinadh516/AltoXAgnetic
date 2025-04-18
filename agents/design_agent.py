from vertexai.generative_models import GenerativeModel, Part

class DesignAgent:
    """
    Analyzes the screenshot and extracts a pixel-perfect, deeply detailed layout/structure.
    """
    def __init__(self, image_bytes, mime_type):
        self.image_bytes = image_bytes
        self.mime_type = mime_type
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def run(self):
        image_part = Part.from_data(mime_type=self.mime_type, data=self.image_bytes)
        prompt = (
            "You are a senior UI/UX designer and frontend engineer. Analyze the uploaded screenshot and extract a pixel-perfect layout specification. "
            "For every visible section (header, navigation bar, sidebar, main content, footer, cards, forms, modals, overlays), provide:\n"
            "- Section name and type\n"
            "- Exact pixel coordinates: x, y, width, height\n"
            "- Spacing: margin, padding, gap between elements (in px)\n"
            "- Alignment: horizontal and vertical alignment, justification\n"
            "- Layout system: grid, flex, absolute, relative, and all breakpoints\n"
            "- Font details: family, size (px), weight, color, line-height, letter-spacing\n"
            "- Colors: background, border, text, accent, hover, active, disabled\n"
            "- Border radius, border width, border color, box-shadow, opacity\n"
            "- Responsive/adaptive hints if visible\n"
            "- Z-index or stacking order if overlays are present\n"
            "Return ONLY a valid JSON object with a list of sections, each with all these details. No explanations, no markdown."
        )
        responses = self.model.generate_content([image_part, prompt], stream=False)
        return responses.text if hasattr(responses, "text") else str(responses)