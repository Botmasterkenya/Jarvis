from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)

_history = []

def ask(user_message: str) -> str:
    """Send a message to Gemini and get a response."""
    global _history

    _history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1024,
                temperature=0.7,
            ),
            contents=_history
        )
        reply = response.text.strip()

        _history.append(
            types.Content(
                role="model",
                parts=[types.Part(text=reply)]
            )
        )

        return reply

    except Exception as e:
        return f"Gemini error: {str(e)}"

def reset_chat():
    """Clear conversation memory."""
    global _history
    _history = []