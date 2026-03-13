import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

print("GROQ KEY LOADED =", os.getenv("GROQ_API_KEY"))


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(user_query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are UNIGuide AI, a helpful university assistant."
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature=0.4,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq LLM Error:", e)
        return "🤖 AI service temporarily unavailable."
