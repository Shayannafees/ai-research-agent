import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("Streaming response:\n")

with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="You are a concise research assistant.",
    messages=[
        {"role": "user", "content": "Explain RAG in simple terms"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print("\n\nDone.")
