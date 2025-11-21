# Function Calling-Based Decision Making with Tool Use
  
"""
demo for:
- LLM function calling (tool_choice) instead of manual JSON parsing
- Automatic tool invocation based on model decisions
- Escalation tool triggered when severity = CRISIS
- Cleaner separation of concerns
- SIMPLIFIED: call model → tool_calls → run tools → show results → stop
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

DEFAULT_TEMPERATURE = 0.1
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
  
    # loop through the actions list while also getting the index of each item
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
      
    # Convert a Python object into a JSON string
    return json.dumps(result)


# -------------------------
# LLM interaction with function calling (SIMPLIFIED)
# -------------------------

def call_triage_llm_with_tools(description: str,
                               temperature: float,
                               max_tokens: int) -> Dict[str, Any]:
    """
    Call LLM with function calling enabled.

    SIMPLIFIED for teaching:
    - Single call to LLM
    - If a tool is called, execute it once
    - Collect summary, severity, actions + ticket info
    """
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
    
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",  # Let model decide when to use tools
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
        )
    except Exception as e:
        print(f"\n[ERROR] Failed to call OpenAI API: {e}")
        sys.exit(1)
    
    msg = response.choices[0].message
    result_data: Dict[str, Any] = {}

    # For teaching: we assume the model always calls our tool once
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]  # Take the first tool in the list
        tool_name = tool_call.function.name  # get the tool name the model wants to call.
        tool_input = json.loads(tool_call.function.arguments)  # convert JSON string into Python dict

        print(f"\n[CALLING] {tool_name}")
        tool_result_json = process_tool_call(tool_name, tool_input)
        tool_result = json.loads(tool_result_json)

        # Fill result_data in a simple, explicit way for teaching
        result_data["summary"] = tool_input.get("summary", "")
        result_data["severity"] = tool_input.get("severity", "")
        result_data["actions"] = tool_input.get("actions", [])
        result_data["escalated"] = tool_result
        result_data["ticket_id"] = tool_result.get("ticket_id")

    else:
        # If, for some reason, no tool was called, we just store the model's text
        result_data["message"] = msg.content or "(no tool call, text response only)"
    
    return result_data


# -------------------------
# Workflow
# -------------------------

def run_workflow_with_function_calling(description: str,
                                       temperature: float,
                                       max_tokens: int) -> None:
    """End-to-end workflow using function calling."""
    print("\n=== Calling LLM with Function Calling ===")
    print(f"(Using temperature={temperature}, max_tokens={max_tokens})")
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
        print("\nIncident triaged and logged (no escalation tool used).")
    
    print("\n=== Workflow Complete ===")


# -------------------------
# Main entry point
# -------------------------

def main() -> None:
    print("=== Incident Triage with Function Calling ===")
    print("This demo uses:")
    print("- LLM function calling (tool_choice)")
    print("- Automatic tool invocation (single step, teaching version)")
    print("- Crisis escalation tool triggered on CRISIS severity\n")

    description = input("Describe the incident: ").strip()
    if not description:
        print("No description provided. Exiting.")
        return

    run_workflow_with_function_calling(description, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS)


if __name__ == "__main__":
    main()

