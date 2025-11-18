# Function Calling-Based Decision Making with Tool Use
  
"""
demo for:
- LLM function calling (tool_choice) instead of manual JSON parsing
- Automatic tool invocation based on model decisions
- Escalation tool triggered when severity = CRISIS
- Cleaner separation of concerns
- Call model → get tool_calls → run tools → send tool results back → call model again → (repeat while there are tool calls)
"""

import json
import sys
import uuid
from typing import List, Dict, Any
import requests
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name

# -------------------------
# Configuration
# -------------------------

DEPLOYMENT_NAME = get_model_deployment_name()

DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 500

USE_REAL_EMAIL = False

# Initialize Azure OpenAI client
client = AzureOpenAI(**get_api_credentials())


# -------------------------
# Tool definitions (function schema)
# -------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "escalate_crisis",
            "description": "Escalate a CRISIS-level incident to on-call team. Generates ticket ID automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Incident summary"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["NORMAL", "ALERT", "CRISIS"],
                        "description": "Severity level"
                    },
                    "actions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Required actions"
                    }
                },
                "required": ["summary", "severity", "actions"]
            }
        }
    }
]

# -------------------------
# Tool implementation functions
# -------------------------

def escalate_crisis(summary: str, severity: str, actions: List[str]) -> Dict[str, Any]:
    """Handle incident - generates ticket ID internally."""
    ticket_id = f"TICKET-{uuid.uuid4().hex[:6].upper()}"
    print(f"\n[TOOL] escalate_crisis called")
    print(f"       Ticket ID: {ticket_id}")
    print(f"       Severity : {severity}")
    print(f"       Summary  : {summary}")
    
    subject = f"[{severity}] {ticket_id} - {summary}"
    body_lines = [
        f"Incident ID: {ticket_id}",
        f"Severity   : {severity}",
        "",
        "Required Actions:",
    ]
    for i, action in enumerate(actions, start=1):
        body_lines.append(f"  {i}. {action}")
    
    print("[EMAIL] Alert:")
    print(f"        Subject: {subject}")
    for line in body_lines:
        print("         ", line)
    
    return {
        "success": True,
        "ticket_id": ticket_id,
        "severity": severity
    }


def process_tool_call(tool_name: str, tool_input: Dict[str, Any]) -> str:
    """Route tool calls to appropriate handler."""
    if tool_name == "escalate_crisis":
        result = escalate_crisis(
            summary=tool_input.get("summary", ""),
            severity=tool_input.get("severity", ""),
            actions=tool_input.get("actions", [])
        )
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    
    return json.dumps(result)


# -------------------------
# LLM interaction with function calling
# -------------------------

def call_triage_llm_with_tools(description: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call LLM with function calling enabled."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are an incident handler. "
                "Analyze incidents and call the escalate_crisis tool to log and handle them. "
                "Use severity: NORMAL for minor issues, ALERT for significant issues, CRISIS for critical issues. "
                "Always call the tool."
            )
        },
        {
            "role": "user",
            "content": (
                f"Incident description:\n{description}\n\n"
                "Analyze this incident and use the appropriate tools."
            )
        }
    ]
    
    # First API call with tool definitions
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",  # Let model decide when to use tools
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:
        print(f"\n[ERROR] Failed to call OpenAI API: {e}")
        sys.exit(1)
    
    # Process tool calls in a loop until no more tools are called
    result_data = {}
    
    while response.choices[0].message.tool_calls:
        tool_calls = response.choices[0].message.tool_calls
        
        # Add assistant response to messages
        # Build a list of dictionaries, one dictionary for each tc in tool_calls
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in tool_calls
            ]
        })
        
        # Process each tool call
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            
            print(f"\n[CALLING] {tool_name}")
            tool_result = process_tool_call(tool_name, tool_input)
            
            # Add tool result as separate message
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
            
            # Store result data
            if tool_name == "escalate_crisis":
                result_data["escalated"] = json.loads(tool_result)
                result_data["ticket_id"] = tool_input.get("ticket_id")
        
        # Call LLM again to continue the conversation
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            print(f"\n[ERROR] Failed in tool call loop: {e}")
            break
    
    return result_data


# -------------------------
# Workflow
# -------------------------

def run_workflow_with_function_calling(description: str, temperature: float, max_tokens: int) -> None:
    """End-to-end workflow using function calling."""
    print("\n=== Calling LLM with Function Calling ===")
    data = call_triage_llm_with_tools(description, temperature, max_tokens)
    
    print("\n=== Workflow Results ===")
    print(f"Summary : {data.get('summary', '(none)')}")
    print(f"Severity: {data.get('severity', '(none)')}")
    print("Actions :")
    for i, action in enumerate(data.get("actions", []), start=1):
        print(f"  {i}. {action}")
    
    if data.get("escalated"):
        print(f"\n✓ Crisis escalated - Ticket: {data.get('ticket_id')}")
    else:
        print("\nIncident triaged and logged.")
    
    print("\n=== Workflow Complete ===")


# -------------------------
# Main entry point
# -------------------------

def main() -> None:
    print("=== Incident Triage with Function Calling ===")
    print("This demo uses:")
    print("- LLM function calling (tool_choice)")
    print("- Automatic tool invocation")
    print("- Crisis escalation tool triggered on CRISIS severity\n")

    description = input("Describe the incident: ").strip()
    if not description:
        print("No description provided. Exiting.")
        return

    # Temperature
    temp_str = input(f"Temperature (default {DEFAULT_TEMPERATURE}): ").strip()
    try:
        temperature = float(temp_str) if temp_str else DEFAULT_TEMPERATURE
    except ValueError:
        print(f"Invalid temperature, using default {DEFAULT_TEMPERATURE}.")
        temperature = DEFAULT_TEMPERATURE

    # Max tokens
    max_tokens_str = input(f"Max tokens (default {DEFAULT_MAX_TOKENS}): ").strip()
    try:
        max_tokens = int(max_tokens_str) if max_tokens_str else DEFAULT_MAX_TOKENS
    except ValueError:
        print(f"Invalid max tokens, using default {DEFAULT_MAX_TOKENS}.")
        max_tokens = DEFAULT_MAX_TOKENS

    run_workflow_with_function_calling(description, temperature, max_tokens)


if __name__ == "__main__":
    main()
