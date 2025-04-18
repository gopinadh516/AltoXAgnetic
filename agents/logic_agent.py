from vertexai.generative_models import GenerativeModel

class LogicAgent:
    """
    Adds interactivity, state management, and API logic to the generated code using Gemini Flash.
    """
    def __init__(self, tech_stack):
        self.tech_stack = tech_stack
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def run(self, code, logic_requirements=None):
        logic_requirements = logic_requirements or (
            "Add form validation (client-side), state management (React hooks or JS objects), "
            "dummy API calls (simulate with setTimeout or async/await), error handling, "
            "and accessibility improvements (aria attributes, keyboard navigation). "
            "Ensure all logic is robust, user-friendly, and matches the UI design exactly."
        )
        prompt = (
            "You are a frontend logic and UX expert. Given this code:\n"
            f"{code}\n"
            f"for the tech stack: {self.tech_stack}\n"
            f"Add the following logic and interactivity: {logic_requirements}\n"
            "- Ensure all form fields are validated with clear error messages\n"
            "- Use state management best practices\n"
            "- Simulate API calls for form submission\n"
            "- Add loading and success/error states\n"
            "- Ensure accessibility and keyboard navigation\n"
            "Return only the updated code, no explanations."
        )
        responses = self.model.generate_content([prompt], stream=False)
        return responses.text if hasattr(responses, "text") else str(responses)