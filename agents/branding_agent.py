from vertexai.generative_models import GenerativeModel

class BrandingAgent:
    """
    Suggests a complete, modern, accessible design system and branding guideline.
    """
    def __init__(self, components, image_bytes=None):
        self.components = components
        self.image_bytes = image_bytes
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def run(self):
        design_system = """
Design System Example:
- Primary Color: #142850
- Secondary Color: #27496d
- Accent Color: #00909e
- Background Color: #f8f8f8
- Surface Color: #ffffff
- Text Color: #222831
- Error Color: #e74c3c
- Success Color: #27ae60
- Warning Color: #f39c12
- Info Color: #2980b9
- Font Family: 'Inter', 'Roboto', Arial, sans-serif
- Font Weights: 400 (regular), 600 (semibold), 700 (bold)
- Font Sizes: 12px, 14px, 16px, 20px, 24px, 32px, 48px
- Line Heights: 1.2, 1.5, 1.75
- Letter Spacing: 0.5px, 1px
- Border Radius: 8px, 16px for cards/modals
- Button Style: Filled, outlined, text, rounded, shadow, primary uses Primary Color, secondary uses Accent Color
- Input Style: Rounded, subtle border, focus uses Accent Color, placeholder color #888
- Spacing: 4px, 8px, 16px, 24px, 32px, 40px
- Shadows: Soft, subtle for cards and modals, elevation levels 1-5
- Accessibility: All color contrast meets WCAG AA, focus indicators visible, keyboard navigation enabled
"""
        prompt = (
            "You are a digital brand designer and design system expert. Given these UI components:\n"
            f"{self.components}\n"
            "and the following design system example:\n"
            f"{design_system}\n"
            "Extract and suggest a modern, accessible color palette (primary, secondary, background, surface, text, accent, error, success, warning, info), "
            "font system (font family, weights, sizes, line heights, letter spacing), and all relevant branding tokens (border radius, shadows, spacing, button/input style, accessibility). "
            "For each color and font, provide the exact hex code or CSS value and where it should be applied. "
            "Return ONLY a valid JSON object with all these details, suitable for direct use in a design system. No explanations, no markdown."
        )
        responses = self.model.generate_content([prompt], stream=False)
        return responses.text if hasattr(responses, "text") else str(responses)