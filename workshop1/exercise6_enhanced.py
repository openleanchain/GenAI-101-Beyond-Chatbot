# 🎯 Enhanced IT Repair AI with Structured JSON Output (Azure OpenAI)
# Uses response_format to guarantee valid JSON responses

from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name
import json

# 2) CREATE THE CLIENT (with credentials) — reusable, credentialed handle
creds = get_api_credentials()
client = AzureOpenAI(**creds)

# Use your Azure deployment name (the model you've deployed in Azure OpenAI)
DEPLOYMENT_NAME = get_model_deployment_name()

def improved_it_support_json(problem: str) -> dict:
    """Enhanced version with structured JSON response format guarantee."""
    # 3) CALL THE SERVICE with response_format to enforce JSON output

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced IT support specialist. "
                    "Extract repair information and return valid JSON only. "
                    "Do not include any text outside the JSON object."
                )
            },
            {"role": "user", "content": problem}
        ],
        response_format={"type": "json_object"},  # ✅ Enforce JSON output
        temperature=0.1,  # Low temperature → consistent, reliable guidance
        max_tokens=1000   # Bound response length for predictable output
    )
    # 4) PROCESS THE RESPONSE — parse JSON and return as dict
    result_text = response.choices[0].message.content
    return json.loads(result_text)

# Test it
user_problem = "Customer's iPhone 12 has cracked screen. Happened yesterday (2025-11-20) when dropped. Touch still works but display shows lines. Customer needs it by Friday."

prompt = f"""
Extract repair information and format as JSON:

Description: "{user_problem}"

Return this JSON structure:
{{
    "device": {{
        "brand": "string",
        "model": "string",
        "type": "phone|laptop|tablet|desktop"
    }},
    "damage": {{
        "primary_issue": "string",
        "symptoms": ["list of symptoms"],
        "cause": "string",
        "date_occurred": "YYYY-MM-DD"
    }},
    "repair": {{
        "complexity": "simple|moderate|complex",
        "parts_needed": ["list"],
        "estimated_cost": "number",
        "estimated_hours": "number"
    }},
    "urgency": {{
        "priority": "low|medium|high|urgent",
        "deadline": "YYYY-MM-DD or null"
    }}
}}
"""

result = improved_it_support_json(prompt)
print(f"User: {user_problem}\n")
print("AI Response (as JSON):")
print(json.dumps(result, indent=2))
