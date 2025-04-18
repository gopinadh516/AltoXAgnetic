from vertexai.generative_models import GenerativeModel

class ComponentAgent:
    """
    Identifies every UI component with exhaustive detail from the layout.
    """
    def __init__(self, layout_info):
        self.layout_info = layout_info
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def run(self):
        prompt = (
            "You are a frontend architect. Given this layout structure:\n"
            f"{self.layout_info}\n"
            "For each section, identify every UI component (button, input, select, dropdown, card, icon, image, avatar, badge, chip, progress bar, slider, modal, tooltip, tab, accordion, list, table, pagination, breadcrumb, alert, snackbar, switch, checkbox, radio, textarea, link, menu, sidebar, navbar, footer, header, stepper, carousel, timeline, calendar, datepicker, timepicker, rating, divider, spinner, loader, overlay, popover, dialog, and any other visible element).\n"
            "For each component, provide:\n"
            "- type\n"
            "- label or placeholder text\n"
            "- icon or image source (if present)\n"
            "- position: x, y, width, height (px)\n"
            "- state: default, hover, active, disabled, focused, checked, unchecked, selected, unselected, expanded, collapsed\n"
            "- parent/child relationships and nesting\n"
            "- accessibility attributes: aria-label, role, tabIndex, alt text\n"
            "- micro-interactions: animation type, trigger, duration, easing\n"
            "- visibility: visible, hidden, collapsed\n"
            "Return ONLY a valid JSON array, one object per component, with all these details. No explanations, no markdown."
        )
        responses = self.model.generate_content([prompt], stream=False)
        return responses.text if hasattr(responses, "text") else str(responses)