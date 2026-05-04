import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(prompt):
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful HR assistant that answers strictly from provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback (VERY IMPORTANT)
        return f"""
[LLM ERROR - FALLBACK RESPONSE]

Reason: {str(e)}

Simulated Answer:
Based on retrieved documents, maternity leave policy typically allows employees around 180 days of leave with certain eligibility conditions.

(Note: This fallback is shown because API quota or connection failed.)
"""