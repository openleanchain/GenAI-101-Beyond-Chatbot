# 1) INSTALL & IMPORT — SDK to talk to the service
#    pip install openai
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

# 2) CREATE THE CLIENT (with credentials)
client = AzureOpenAI(**get_api_credentials())

# Use your Azure deployment name (the model you've deployed in Azure OpenAI)
DEPLOYMENT_NAME = get_model_deployment_name()

def basic_it_support(problem):
    """Most basic version - just works!"""
    # 3) CALL THE SERVICE (Chat Completion) — send prompt with deployment name
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": problem}],
        max_tokens=50
    )
    # 4) PROCESS THE RESPONSE — extract assistant message
    return response.choices[0].message.content


# Test it!
print("Hello, how can I help you? (type 'quit' to exist.)")
while True:
    user_input = input("User: ")
    if user_input and len(user_input.strip())>0 and user_input.lower() != "quit":
        result = basic_it_support(user_input)
        print(f"AI: {result}")
    else:
        break
print("AI: bye.")
