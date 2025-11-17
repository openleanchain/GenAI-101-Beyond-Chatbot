from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

def run_chat_loop(system_prompt=None):
    client = AzureOpenAI(**get_api_credentials())

    DEPLOYMENT_NAME = get_model_deployment_name()

    if system_prompt is None:
        system_prompt = "You are an IT support specialist. Ask clarifying questions."

    messages = [{"role": "system", "content": system_prompt}]

    print("Interactive chat. Type 'exit' or 'quit' to stop, 'reset' to clear conversation.")
    try:
        while True:
            user_input = input("User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting.")
                break
            if user_input.lower() == "reset":
                messages = [{"role": "system", "content": system_prompt}]
                print("Conversation reset.")
                continue
            if user_input.lower() == "show history":
                for m in messages:
                    print(f"{m['role']}: {m['content']}")
                continue

            messages.append({"role": "user", "content": user_input})

            try:
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=messages
                )
                assistant_text = response.choices[0].message.content
            except Exception as e:
                print(f"API error: {e}")
                # remove last user message on error or keep depending on desired behavior
                messages.pop()
                continue

            print(f"*******************\nAI: {assistant_text}")
            messages.append({"role": "assistant", "content": assistant_text})

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")

if __name__ == "__main__":
    run_chat_loop()
