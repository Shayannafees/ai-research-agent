import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation = []

def chat(user_message):
    conversation.append({"role": "user", "content": user_message})
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="You are a research assistant helping build an AI project.",
        messages=conversation
    )
    
    assistant_message = response.content[0].text
    conversation.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

print(chat("What is LangChain?"))
print("\n---\n")
print(chat("How does it compare to building with the raw API?"))
print("\n---\n")
print(chat("Which should I use for a research agent?"))
