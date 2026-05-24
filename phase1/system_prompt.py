import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="""You are a research assistant that always responds in structured JSON.
For any topic, return exactly this structure:
{
  "summary": "2-3 sentence summary",
  "key_points": ["point1", "point2", "point3"],
  "follow_up_questions": ["question1", "question2"]
}
Return only valid JSON, no extra text, no markdown.""",
    messages=[
        {"role": "user", "content": "Research topic: Large Language Models"}
    ]
)

raw = message.content[0].text
clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
data = json.loads(clean)
print(json.dumps(data, indent=2))
