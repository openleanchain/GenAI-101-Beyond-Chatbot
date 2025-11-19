# Manual JSON-Based Decision Making
  
"""
demo for:
- Prompt engineering with few-shot examples
- JSON-only output (response_format = json_object)
- Simple end-to-end workflow orchestration:
  - LLM triage
  - Ticket creation (simulated)
  - "Save to DB" (simulated)
  - Email escalation (simulated or real via SMTP)
"""

import json
import os
import sys
import uuid
from typing import List, Dict, Any
import requests
import json
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name, get_email_receiver, get_email_api_info

# -------------------------
# Configuration
# -------------------------

DEPLOYMENT_NAME = get_model_deployment_name()

DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 200

# Toggle: if False, email is only simulated (printed to console)
USE_REAL_EMAIL = False  # True  False

# Initialize Azure OpenAI client (with credentials) — reusable, credentialed handle
client = AzureOpenAI(**get_api_credentials())


# -------------------------
# Utility functions
# -------------------------

def severity_score(severity: str) -> int:
    """Map severity label to a numeric score for display."""
    mapping = {"NORMAL": 25, "ALERT": 65, "CRISIS": 95}
    return mapping.get(severity.upper(), 25)


def build_messages(description: str) -> List[Dict[str, Any]]:
    """
    Build chat messages with:
    - System message
    - Two few-shot examples (NORMAL + CRISIS)
    - The current incident
    """
    system_msg = {
        "role": "system",
        "content": (
            "You are a concise incident triage assistant. "
            "Always reply with a single JSON object only."
        ),
    }

    # Few-shot example 1 (NORMAL)
    example_user_1 = {
        "role": "user",
        "content": (
            "Incident description:\n"
            "Some users report a slightly slow page load on the intranet homepage."
        ),
    }
    example_assistant_1 = {
        "role": "assistant",
        "content": json.dumps({
            "summary": "Minor slowdown on intranet homepage for some users.",
            "severity": "NORMAL",
            "actions": [
                "Log the incident in the monitoring system.",
                "Check recent performance dashboards.",
                "Monitor for any worsening or new complaints."
            ]
        })
    }

    # Few-shot example 2 (CRISIS)
    example_user_2 = {
        "role": "user",
        "content": (
            "Incident description:\n"
            "Production database is down, no connections possible from any app."
        ),
    }
    example_assistant_2 = {
        "role": "assistant",
        "content": json.dumps({
            "summary": "Production database outage blocking all applications.",
            "severity": "CRISIS",
            "actions": [
                "Page on-call DB engineer immediately.",
                "Fail over to backup database if available.",
                "Post incident update on status page.",
                "Notify leadership about business impact."
            ]
        })
    }

    # Current user incident
    current_user = {
        "role": "user",
        "content": (
            "Incident description:\n"
            f"{description}\n\n"
            "Return ONLY a JSON object with keys: summary, severity, actions. "
            "severity must be one of: NORMAL, ALERT, CRISIS. "
            "actions must be a list of 3-5 concrete next steps."
        )
    }

    return [
        system_msg,
        example_user_1, example_assistant_1,
        example_user_2, example_assistant_2,
        current_user,
    ]


def call_triage_llm(description: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call the chat completion API in JSON mode and return a Python dict."""
    messages = build_messages(description)

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:
        print("\n[ERROR] Failed to call OpenAI API:")
        print(f"        {e}")
        sys.exit(1)

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("\n[ERROR] Model did not return valid JSON:")
        print(f"        Raw content: {content!r}")
        print(f"        JSON error : {e}")
        sys.exit(1)

    # Basic validation
    if not isinstance(data, dict):
        print("\n[ERROR] JSON response is not an object:")
        print(f"        {data!r}")
        sys.exit(1)

    # Ensure expected keys exist (with fallbacks)
    data.setdefault("summary", "(no summary)")
    data.setdefault("severity", "NORMAL")
    data.setdefault("actions", [])

    if not isinstance(data["actions"], list):
        data["actions"] = [str(data["actions"])]

    return data


# -------------------------
# Workflow steps
# -------------------------

def create_ticket_incident(summary: str, severity: str) -> str:
    """Simulate creating a ticket in a system."""
    ticket_id = f"TICKET-{uuid.uuid4().hex[:6].upper()}"
    print(f"[WORKFLOW] Creating ticket {ticket_id} ({severity}) - {summary}")
    return ticket_id


def save_to_db_placeholder(ticket_id: str, description: str, data: Dict[str, Any]) -> None:
    """Simulate saving the incident to a database."""
    print(f"[WORKFLOW] (DB) Saving ticket {ticket_id} to database (simulated).")
    # You could write to a local JSON file here in a real exercise.


def _send_real_email(subject: str, body: str) -> None:
    """
    Only used if USE_REAL_EMAIL = True.
    """
    API_URL, API_KEY = get_email_api_info()
    print(f"[EMAIL] Sending real email to: {API_URL}")
    email_receiver = json.loads(get_email_receiver())

    payload = {
        "to": email_receiver,
        "subject": subject,
        "body": body
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    print("Status: ", response.status_code)
    print("Response JSON:", response.json())



def send_email_alert(ticket_id: str, severity: str, summary: str, actions: List[str]) -> None:
    """Either simulate or actually send an email alert."""
    subject = f"[{severity}] Incident {ticket_id} - {summary}"
    body_lines = [
        f"Incident ID: {ticket_id}",
        f"Severity   : {severity}",
        "",
        "Recommended actions:",
    ]
    for i, action in enumerate(actions, start=1):
        body_lines.append(f"  {i}. {action}")
    body = "\n".join(body_lines)

    if USE_REAL_EMAIL:
        print("[EMAIL] Sending real email...")
        _send_real_email(subject, body)
        print("[EMAIL] Email sent (or attempted).")
    else:
        print("[EMAIL] (Simulated) Would send email with:")
        print(f"        Subject: {subject}")
        print("        Body:")
        for line in body_lines:
            print("         ", line)


def maybe_escalate_to_email(ticket_id: str, data: Dict[str, Any]) -> None:
    """Decide whether to escalate via email based on severity."""
    severity = str(data.get("severity", "NORMAL")).upper()
    if severity in ("ALERT", "CRISIS"):
        send_email_alert(ticket_id, severity, data.get("summary", ""), data.get("actions", []))
    else:
        print("[WORKFLOW] No email escalation needed for NORMAL severity.")


def run_workflow(description: str, temperature: float, max_tokens: int) -> None:
    """End-to-end workflow: triage → ticket → DB → email → dashboard."""
    print("\n=== Calling LLM for triage ===")
    data = call_triage_llm(description, temperature, max_tokens)

    sev = str(data.get("severity", "NORMAL")).upper()
    score = severity_score(sev)

    print("\n=== LLM JSON Response ===")
    print(f"Summary : {data.get('summary')}")
    print(f"Severity: {sev} ({score}/100)")
    print("Actions :")
    for i, action in enumerate(data.get("actions", []), start=1):
        print(f"  {i}. {action}")

    print("\n=== Orchestrating Workflow ===")
    ticket_id = create_ticket_incident(data.get("summary", ""), sev)
    save_to_db_placeholder(ticket_id, description, data)
    maybe_escalate_to_email(ticket_id, data)
    print("[WORKFLOW] Updating dashboards (simulated).")

    print("\n=== Workflow Complete ===")
    print(f"Ticket ID: {ticket_id}")
    print("Done.")


# -------------------------
# Main entry point
# -------------------------

def main() -> None:
    print("=== Incident Triage Console Demo ===")
    print("This demo uses:")
    print("- Few-shot prompt engineering")
    print("- JSON-only output (response_format = json_object)")
    print("- Simple end-to-end workflow (ticket + DB + email)\n")

    description = input("Describe the incident: ").strip()
    if not description:
        print("No description provided. Exiting.")
        return

    # Temperature
    temp_str = input(f"Temperature (default {DEFAULT_TEMPERATURE}): ").strip()
    try:
        temperature = float(temp_str) if temp_str else DEFAULT_TEMPERATURE
    except ValueError:
        print(f"Invalid temperature '{temp_str}', using default {DEFAULT_TEMPERATURE}.")
        temperature = DEFAULT_TEMPERATURE

    # Max tokens
    max_tokens_str = input(f"Max tokens (default {DEFAULT_MAX_TOKENS}): ").strip()
    try:
        max_tokens = int(max_tokens_str) if max_tokens_str else DEFAULT_MAX_TOKENS
    except ValueError:
        print(f"Invalid max tokens '{max_tokens_str}', using default {DEFAULT_MAX_TOKENS}.")
        max_tokens = DEFAULT_MAX_TOKENS

    run_workflow(description, temperature, max_tokens)


if __name__ == "__main__":
    main()

  

