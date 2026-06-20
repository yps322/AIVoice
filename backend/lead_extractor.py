import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

EXTRACT_PROMPT = """
You are an insurance lead extraction engine.

Analyze the conversation and extract lead information.

Return ONLY valid JSON.

Schema:

{
    "name": "",
    "age": "",
    "city": "",
    "phone": "",
    "email": "",
    "insurance_type": "",
    "health_info": "",
    "qualified": false,
    "handoff_required": false
}

Rules:
- Return only JSON.
- Do not include markdown.
- Do not include explanations.
- Do not invent information.
- If information is not available, return an empty string.
- qualified should be true only if:
  - user has shown interest in insurance, AND
  - at least a name or contact detail is available.
- handoff_required should be true only if the user explicitly asks to talk to a human agent, representative, or requests a callback later.
"""

def extract_lead(conversation_text: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": EXTRACT_PROMPT
            },
            {
                "role": "user",
                "content": conversation_text
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown if model returns it
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        lead_data = json.loads(content)

        return {
            "name": lead_data.get("name", ""),
            "age": lead_data.get("age", ""),
            "city": lead_data.get("city", ""),
            "phone": lead_data.get("phone", ""),
            "email": lead_data.get("email", ""),
            "insurance_type": lead_data.get("insurance_type", ""),
            "health_info": lead_data.get("health_info", ""),
            "qualified": lead_data.get("qualified", False),
            "handoff_required": lead_data.get("handoff_required", False)
        }

    except Exception as e:

        print("Lead Extraction Error:", e)
        print("Raw Response:", content)

        return {
            "name": "",
            "age": "",
            "city": "",
            "phone": "",
            "email": "",
            "insurance_type": "",
            "health_info": "",
            "qualified": False,
            "handoff_required": False
        }