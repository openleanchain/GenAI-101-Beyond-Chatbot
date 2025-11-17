# 🚀 Your First IT Support AI - Basic Version (Azure OpenAI)
# ⚠️ Demo note: key is hardcoded for simplicity. In production, use env vars or Key Vault.

# 1) INSTALL & IMPORT — SDK to talk to the service
#    pip install openai
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

# 2) CREATE THE CLIENT (with credentials)
# client = AzureOpenAI(**get_api_credentials())
creds = get_api_credentials()
client = AzureOpenAI(
    api_key=creds.get("api_key"),
    azure_endpoint=creds.get("azure_endpoint"),
    api_version=creds.get("api_version")
)

user_problem = "My computer won't turn on"

# 3) CALL THE SERVICE (Chat Completion) — send prompt with deployment name
# Use your Azure deployment name (the model you've deployed in Azure OpenAI)
DEPLOYMENT_NAME = get_model_deployment_name()

"""Most basic version - just works!"""
# Call the service (Chat Completion)
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=[{"role": "user", "content": user_problem}]
)

# 4) PROCESS THE RESPONSE — extract assistant message
result = response.choices[0].message.content

print(f"User: {user_problem}")
print(f"AI: {result}")
