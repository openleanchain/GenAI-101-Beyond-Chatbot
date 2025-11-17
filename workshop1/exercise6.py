# 🎯 Improved IT Support AI with Role & Temperature (Azure OpenAI)
# ⚠️ Demo note: key is hardcoded for simplicity. In production, use env vars or Key Vault.

# 1) INSTALL & IMPORT — SDK to talk to the service
#    pip install openai
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

# 2) CREATE THE CLIENT (with credentials) — reusable, credentialed handle
creds = get_api_credentials()
client = AzureOpenAI(**creds)

# Use your Azure deployment name (the model you've deployed in Azure OpenAI)
DEPLOYMENT_NAME = get_model_deployment_name()

def improved_it_support(problem: str) -> str:
    """Professional version with system role, low temperature, and token limit."""
    # 3) CALL THE SERVICE (Chat Completion) — send prompt with deployment name

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced IT support specialist. "
                    "Provide clear, step-by-step solutions. "
                    "Be patient and thorough."
                )
            },
            {"role": "user", "content": problem}
        ],
        temperature=0.1,  # Low temperature → consistent, reliable guidance
        max_tokens=500    # Bound response length for predictable output
    )
    # 4) PROCESS THE RESPONSE — extract assistant message
    return response.choices[0].message.content

# Test it
# user_problem = "My computer won't turn on"
# user_problem = "Customer's iPhone 12 has cracked screen. Happened yesterday when dropped. Touch still works but display shows lines. Customer needs it by Friday."
user_problem = "Customer's iPhone 12 has cracked screen. Happened yesterday (2025-11-20) when dropped. Touch still works but display shows lines. Customer needs it by Friday."

# change 1: add prompt here and change { to double {{
prompt = f"""
Extract repair information and format as JSON:

Description: "{user_problem}"

Schema:
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
        "estimated_cost": number,
        "estimated_hours": number
    }},
    "urgency": {{
        "priority": "low|medium|high|urgent",
        "deadline": "YYYY-MM-DD or null"
    }}
}}
"""

# change 2: pass prompt instead of user_problem
result = improved_it_support(prompt)
print(f"User: {user_problem}")
print(f"AI: {result}")
