# IMPORT — SDK to talk to the service
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

# 2) CREATE THE CLIENT (with credentials)
client = AzureOpenAI(**get_api_credentials())

# Use your Azure deployment name (the model you've deployed in Azure OpenAI)
DEPLOYMENT_NAME = get_model_deployment_name()  # e.g., "my-gpt4o-mini-deploy"

# Initialize conversation with system message
messages = [
    {
        "role": "system",
        "content": "You are an IT support specialist. Ask clarifying questions."
    }
]
print("Hello, how can I help you? ")

# First user message
user_message = "My computer is slow"
messages.append({
    "role": "user",
    "content": user_message
})
print(f"User: {user_message}")

# Get AI response
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=messages
)
result = response.choices[0].message.content
print(f"AI: {result}")

# Add AI response to conversation
messages.append({
    "role": "assistant",
    "content": result
})

# Continue conversation - AI remembers previous conversation!
# Second user message
user_message = "It started after Windows update"
messages.append({
    "role": "user",
    "content": user_message
})
print(f"User: {user_message}")

# Get AI response
# AI can now reference "slow computer" AND "Windows update"
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=messages
)
result = response.choices[0].message.content
print(f"AI: {result}")

# Add AI response to conversation
messages.append({
    "role": "assistant",
    "content": result
})
