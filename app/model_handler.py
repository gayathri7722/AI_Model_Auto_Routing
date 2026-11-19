
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_response(question, model):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Error: Groq API key not found."

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_completion_tokens=4096
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"
