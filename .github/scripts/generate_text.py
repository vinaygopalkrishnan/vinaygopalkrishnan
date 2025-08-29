import os
import google.generativeai as genai
import re

# Get API key from environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# Gemini prompt to generate a short, clever message
prompt = """
Generate a single, short, inspirational, and creative quote or thought of the day related to coding, technology, or personal growth. Make it sound unique and not like a generic quote.

Example 1: The best code is written with a purpose, not just a plan.
Example 2: Every bug is an opportunity to learn the language you thought you knew.
Example 3: Your most powerful tool isn't your IDE, it's your curiosity.

Do not include any quotation marks in the output.
"""

response = model.generate_content(prompt)
generated_text = response.text.strip()

# Read the existing README.md content
with open('README.md', 'r') as f:
    readme_content = f.read()

# Find and replace the dynamic section
# Define markers
start_marker = "<!-- GEMINI_QUOTE_START -->"
end_marker = "<!-- GEMINI_QUOTE_END -->"

if start_marker in readme_content and end_marker in readme_content:
    new_readme_content = re.sub(
        f'{start_marker}.*{end_marker}',
        f'{start_marker}\n> **💡 Thought of the Day:** {generated_text}\n\n{end_marker}',
        readme_content,
        flags=re.DOTALL
    )

    with open('README.md', 'w') as f:
        f.write(new_readme_content)
else:
    print("Markers not found in README.md. Please add them.")