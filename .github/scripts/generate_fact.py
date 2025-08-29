import os
import google.generativeai as genai

PROMPT = "Generate a short, fascinating fact about computer science, software, or technology history."
FACT_FILE = "FACT.md"
HEADER = "### 💡 Daily Tech Fact\n\n"
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

    with open(FACT_FILE, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write(fact + "\n")

if __name__ == "__main__":
    main()