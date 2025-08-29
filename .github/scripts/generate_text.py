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

# Fetch the content from the Gemini API
try:
    response = model.generate_content(prompt, stream=False)
    # Check if the response contains any text before proceeding
    if response.text:
        generated_text = response.text.strip()
    else:
        # Fallback in case the API returns an empty response
        generated_text = "The journey of a thousand lines begins with a single commit."
except Exception as e:
    print(f"An error occurred while calling the Gemini API: {e}")
    # Provide a static fallback quote
    generated_text = "Progress, not perfection, is the goal of every line of code."

# Read the existing README.md content
readme_path = 'README.md'
if not os.path.exists(readme_path):
    print(f"Error: {readme_path} not found.")
    exit(1)

# Ensure the generated text fits on a single line for better display
generated_text = generated_text.replace('\n', ' ').replace('\r', '')

# Read the existing README.md content
with open(readme_path, 'r') as f:
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