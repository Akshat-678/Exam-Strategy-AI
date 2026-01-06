import os
import json
from google import genai
from google.genai import types

# Initialize the client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Using the 2.5 Flash model as requested
MODEL_NAME = "gemini-2.5-flash"

def analyze_question_paper(text: str):
    prompt = f"""
    Analyze the following exam paper text.
    1. Identify the core topics and their percentage weightage.
    2. Rate the overall difficulty (0-100).
    3. Based on the weightage, provide 3-4 actionable 'Writing Tips' to help the user 
       maximize marks (e.g., 'Focus on Topic X as it covers 40% of the paper').

    Return ONLY a valid JSON object with this structure:
    {{
      "topics": {{ "Topic Name": percentage_integer }},
      "difficulty_score": integer,
      "writing_tips": ["string tip 1", "string tip 2"]
    }}

    Exam Text:
    {text}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )

        if not response.text:
            raise ValueError("Model returned an empty response.")

        return json.loads(response.text)

    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "topics": {"Error": 100},
            "difficulty_score": 0,
            "writing_tips": ["Could not generate tips. Please check the input text."]
        }