# 🎯 Improved IT Support AI with Role & Temperature (Azure OpenAI)
# ⚠️ Demo note: key is hardcoded for simplicity. In production, use env vars or Key Vault.

# 1) INSTALL & IMPORT — SDK to talk to the service
#    pip install openai
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

# 2) CREATE THE CLIENT (with credentials) — reusable, credentialed handle
client = AzureOpenAI(**get_api_credentials())

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
        max_tokens=100    # Bound response length for predictable output
    )
    # 4) PROCESS THE RESPONSE — extract assistant message
    return response.choices[0].message.content

# Test it
user_problem = "My computer won't turn on"
result = improved_it_support(user_problem)
print(f"User: {user_problem}")
print(f"AI: {result}")
