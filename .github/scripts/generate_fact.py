import os
import google.generativeai as genai
import re

PROMPT = "Generate a short, fascinating fact about computer science, software, or technology history."
readme_path = "README.md"
FALLBACK = "The first computer mouse, invented by Douglas Engelbart, was made of wood."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    generative_model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    if not api_key:
        fact = FALLBACK
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(generative_model)
            response = model.generate_content(PROMPT)
            fact = response.text.strip() if response.text else FALLBACK
        except Exception as e:
            fact = FALLBACK

    # Read the existing README.md content
    with open(readme_path, 'r') as f:
        readme_content = f.read()

    start_marker = "<!-- START_FACT -->"
    end_marker = "<!-- END_FACT -->"
    if start_marker in readme_content and end_marker in readme_content:
        new_readme_content = re.sub(
            f'{start_marker}.*{end_marker}',
            f'{start_marker}\n> **💡 Did you know?** {fact}\n\n{end_marker}',
            readme_content,
            flags=re.DOTALL
        )
    with open(readme_path, "w") as f:
        f.write(new_readme_content)

if __name__ == "__main__":
    main()