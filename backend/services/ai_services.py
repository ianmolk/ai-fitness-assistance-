import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_chat_reply(message: str) -> str:
    if not message or not message.strip():
        return "Please enter a message."

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are a helpful fitness assistant. Give safe, practical advice."},
            {"role": "user", "content": message}
        ]
    )

    # Extract text
    text = ""
    for item in response.output:
        if item.type == "message":
            for c in item.content:
                if c.type == "output_text":
                    text += c.text

    return text.strip() or "No response returned."