# IT Repair Hero Academy — Prompt Engineering for Beginners

**Purpose:** This repository stores the **training content** for a beginner-friendly course on **prompt engineering**. To make learning practical and fun, the course uses **IT incident triage & support** as the running use case.

**Audience:** Anyone new to GenAI—students, educators, and working professionals.

**Install:** **Not required.** These materials are for teaching and practice (examples, exercises, and homework). The optional HTML pages support in-class demos in a browser.

---

## Your Mission Objectives
Use these as the four learning pillars for the course.

- **Master Prompts** — *Learn to write effective prompts that get the results you need.*
- **Memory Power** — *Keep multi-turn chats on track with conversation memory.*
- **Structure Output** — *Control how your AI formats and organizes responses.*
- **Integration Hero** — *Turn results into actions beyond the chatbot, such as create tickets, send emails, and call tools when severity requires.*

---

## Course Map

1. **Introduction**  
   **What you do:** Get oriented, review goals, and complete a short pre‑flight to unlock the journey.  
   **Outcome:** Understand the end‑to‑end flow we’ll practice (tiny script → roles → memory → templates → JSON → actions → graduation).

2. **First Contact**  
   **Focus:** Single‑turn prompting fundamentals and **role framing** (system, user, assistant). Start from a tiny “Fix my computer” script, then improve it with role + tone + constraints.  
   **Outcome:** Craft clear, goal‑aligned prompts that steer reliable first answers.

3. **Memory Power**  
   **Focus:** **Multi‑turn prompting**—carry forward key details, restate goals, and keep the conversation on track by appending/curating history.  
   **Outcome:** Design short, iterative prompts that remember what matters across turns.

4. **Structure Master**  
   **Focus:** Schema‑first prompting and **JSON outputs** (stable keys, enums, constraints) for reliable reuse.  
   **Outcome:** Produce machine‑readable responses that are easy to validate and feed into tools.

5. **Integration Hero**  
   **Focus:** Go **beyond the chatbot.** Use structured outputs (e.g., severity) to trigger actions such as ticket creation, email/SMS escalation, on‑call notifications, or simple function calls.  
   **Outcome:** Turn answers into safe, auditable steps that plug into existing IT workflows.

6. **Graduation**  
   **Focus:** Wrap‑up and next steps. Complete the capstone and an **8‑question quiz** (≈2 per section) to earn a certificate.  
   **Outcome:** A clean set of reusable prompts/templates plus a plan for what to learn next (e.g., RAG/Context).

> **Note on terminology:** In this course, “memory” refers to conversation history for multi-turn prompts. A separate RAG course will cover a broader view of memory and context, including external documents and retrieval..

---

## Repository Structure

```
/docs                 # Facilitator notes, pacing guides, answer keys (grows over time)
/exercises            # In‑class tasks and mini‑projects
/homework             # Short homework prompts & instructions
/src                  # Small, self‑contained code snippets used in demos/examples

```

**Important:** The src files are **teaching aids** for live demos. Participants are **not** expected to install or deploy an application.

---

## How to Use This Repo

- **Learners:** Go to the [Online Training](https://ricebot.pythonanywhere.com/bcamp/) 
 and follow each section’s step by step guide and exercises. Use the REPL only to access resources. In instructor led sessions, your facilitator will open the same HTML pages in a browser and guide you in real time.  
- **Facilitators:** coming soon.  

---

## Progress & Gamification

Each section uses simple, visible completion cues (time on task, milestones, and three small challenges where applicable). Learners see checkmarks/toasts during progress and a short “you’re ready for the next section” message. The final capstone plus quiz unlocks a certificate.

---

## License

Use a permissive license (e.g., **MIT**) to encourage educational reuse. Add `LICENSE` at the project root.
