from vertexai.generative_models import GenerativeModel

class CodeAgent:
    """
    Generates frontend code (HTML/CSS/React) from components and branding using Gemini Flash.
    Uses highly detailed, tech-specific prompts for pixel-perfect accuracy.
    """
    def __init__(self, tech_stack, branding=None):
        self.tech_stack = tech_stack
        self.branding = branding or ""
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def get_prompt(self, components):
        base_prompt = (
            "Task: You are an expert web developer tasked with creating a single-page app from a given screenshot using the specified technology stack. "
            "Ensure the app precisely matches the screenshot visually, including layout structure, grid, container, fluid-containers, rows, columns, background color, text color, font size, font family, padding, margin, and alignment. "
            "Double check the colour code and should match with given screenshot visually, I'm expecting 100% match.\n"
            f"Components: {components}\n"
            f"Branding: {self.branding}\n"
        )
        if self.tech_stack == "HTML5 + Tailwind":
            return base_prompt + """
You are an expert HTML5 and Tailwind developer.
- Build a single page app using HTML5 and Tailwind CSS.
- Use <script src="https://cdn.tailwindcss.com"></script> for Tailwind.
- Use placeholder images from https://placehold.co and detailed alt text.
- Do not include markdown or code fences.
- Optimize CSS in <style> and minimize.
- Return the full code in <html></html> tags.
"""
        elif self.tech_stack == "HTML5 + CSS":
            return base_prompt + """
You are an expert HTML5 and CSS developer.
- Build a single page app using HTML5 and CSS.
- Use placeholder images from https://placehold.co and detailed alt text.
- Do not include markdown or code fences.
- Optimize CSS in <style> and minimize.
- Return the full code in <html></html> tags.
"""
        elif self.tech_stack == "HTML5 + Bootstrap5":
            return base_prompt + """
You are an expert HTML5 and Bootstrap 5 developer.
- Build a single page app using HTML5 and Bootstrap 5.
- Use <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"> for Bootstrap.
- Use Bootstrap classes for layout, do not repeat CSS in <style>.
- Use placeholder images from https://placehold.co and detailed alt text.
- Do not include markdown or code fences.
- Return the full code in <html></html> tags.
"""
        elif self.tech_stack == "React + Tailwind":
            return base_prompt + """
You are an expert React and Tailwind developer.
- Build a single page app using React and Tailwind CSS.
- Use scripts for React and Tailwind as needed.
- Use placeholder images from https://placehold.co and detailed alt text.
- Do not include markdown or code fences.
- Optimize CSS and minimize.
- Return the full code in <html></html> tags.
"""
        elif self.tech_stack == "Ionic + Tailwind":
            return base_prompt + """
You are an expert Ionic and Tailwind developer.
- Build a single page app using Ionic and Tailwind CSS.
- Use scripts for Ionic and Tailwind as needed.
- Use placeholder images from https://placehold.co and detailed alt text.
- Do not include markdown or code fences.
- Optimize CSS and minimize.
- Return the full code in <html></html> tags.
"""
        else:
            return base_prompt

    def run(self, components):
        prompt = self.get_prompt(components)
        responses = self.model.generate_content([prompt], stream=False)
        return responses.text if hasattr(responses, "text") else str(responses)