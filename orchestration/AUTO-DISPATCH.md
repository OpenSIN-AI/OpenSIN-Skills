# SIN-Orchestrator: Autonomous Parallel Dispatch Protocol

> **Version 1.0** | **Zero-Human Mandate** | **Infinite Fleet Scaling**

## The Core Principle

**One user. One message. Unlimited parallel agents.**

The user speaks to exactly ONE agent — the **SIN-Orchestrator** (God Agent).
The God Agent decomposes ANY request into parallel tasks, dispatches them across
the entire 126-agent fleet simultaneously, synthesizes results, and delivers
a unified answer. The user never sees the fleet. The user never waits.

## Dispatch Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (single chat)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              SIN-ORCHESTRATOR (God Agent)                    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐ │
│  │    INTENT     │  │    FLEET     │  │   SKILL ROUTER    │ │
│  │  CLASSIFIER   │→│   REGISTRY   │→│   (280+ skills)   │ │
│  └──────────────┘  └──────────────┘  └───────────────────┘ │
│         │                                      │            │
│         ▼                                      ▼            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          PARALLEL DISPATCH ENGINE                    │   │
│  │                                                     │   │
│  │  dispatch([                                         │   │
│  │    {agent: "Code-Frontend", task: "...", bg: true}, │   │
│  │    {agent: "Research",      task: "...", bg: true}, │   │
│  │    {agent: "Telegram",      task: "...", bg: true}, │   │
│  │    {agent: "Security-Web",  task: "...", bg: true}, │   │
│  │  ])                                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          RESULT SYNTHESIZER                          │   │
│  │                                                     │   │
│  │  Merge + Deduplicate + Quality Gate + Format        │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
                   USER ← Answer
```

## The 7-Step Dispatch Loop

Every user message triggers this exact sequence:

### Step 1: Intent Classification
Classify the user's request into one or more domain categories from the fleet registry.
A single request can map to multiple domains (e.g., "build a landing page and post it on Twitter" = coding + social_media).

### Step 2: Agent Selection
For each identified domain, select the most specific agent(s) from fleet-registry.json.
Use keyword matching against the registry's keyword lists.
Prefer specialized agents over generic ones (e.g., A2A-SIN-Code-Frontend over Code-Fullstack for a UI task).

### Step 3: Skill Attachment
For each selected agent, attach the most relevant skills from the 280+ skill library.
Knowledge skills (engineering/, product-team/, etc.) provide CONTEXT.
Operational skills (operations/) provide ACTION PATTERNS.

### Step 4: Task Decomposition
Break the user's request into atomic, parallelizable sub-tasks.
Each sub-task gets assigned to exactly one agent.
Dependencies between tasks are resolved into sequential chains.

### Step 5: Parallel Dispatch
Fire all independent sub-tasks simultaneously using `call_omo_agent(run_in_background=true)`.
Store all task_ids for monitoring.

```python
# Pseudo-code for parallel dispatch
dispatches = []
for task in independent_tasks:
    result = call_omo_agent(
        description=task.title,
        prompt=task.full_spec,
        subagent_type=task.agent_type,
        run_in_background=True
    )
    dispatches.append(result.task_id)
```

### Step 6: Result Collection
Poll all background tasks. Merge results as they complete.
If any task fails, auto-retry with a different agent from the same domain.
If the retry also fails, escalate to the Self-Healing Loop (create GitHub Issue, dispatch fix).

### Step 7: Synthesis & Delivery
Combine all results into a single coherent answer.
Apply quality gates: completeness check, consistency check, format check.
Deliver to user. Log to ledger.

## Dispatch Rules

### Rule 1: Maximum Parallelism
If two tasks have no dependency, they MUST run in parallel. Never serialize independent work.

### Rule 2: Team Escalation
If a single agent can't handle a task, escalate to the Team Manager (Team-SIN-*).
The Team Manager can orchestrate multiple agents within its domain.

### Rule 3: Cross-Domain Chaining
When a task spans multiple domains, use A2A Chain pattern:
Agent A (domain 1) → output → Agent B (domain 2) → output → Agent C (domain 3)

### Rule 4: Self-Healing on Failure
Any failed dispatch triggers:
1. Auto-retry with alternate agent
2. If retry fails: create GitHub Issue with full error context
3. Dispatch issue to Team-SIN-Code-Core for fix
4. Notify user via A2A-SIN-Telegram

### Rule 5: Skill-Augmented Prompts
Every dispatch prompt MUST include relevant skill content.
Don't just say "build a frontend" — attach the engineering/frontend-architecture SKILL.md content.

### Rule 6: Never Ask the User
The God Agent NEVER asks the user for clarification if the answer can be inferred
from context, fleet capabilities, or skill knowledge. Only ask when genuinely ambiguous
AND no reasonable default exists.

### Rule 7: Progress Broadcasting
For long-running tasks (>30s), send progress updates to the user proactively.
Use A2A-SIN-Telegram for out-of-band notifications if the user isn't actively watching.

## Intent-to-Domain Mapping Examples

| User Says | Domains | Agents Dispatched |
|-----------|---------|-------------------|
| "Build me a website" | coding | Code-Frontend, Code-Backend, Code-DevOps |
| "Post about our launch" | social_media, forums | X-Twitter, LinkedIn, HackerNews, ProductHunt |
| "Send a message to John" | messaging | WhatsApp or Telegram or SMS (auto-detect) |
| "Audit our security" | security | Security-Web, Security-Network, Security-Cloud, Security-Audit |
| "File a patent" | legal | Patents, ClaimWriter, Compliance |
| "Set up payments" | commerce | Stripe, Shop-Finance |
| "Research competitors" | research | Research, Summary |
| "Schedule a meeting" | apple | Apple-Calendar-Contacts |
| "Earn some money" | money | Worker-Prolific, Worker-heypiggy, Mindrift |
| "Build a website, post on Twitter, and notify me on Telegram" | coding + social + messaging | Code-Frontend + X-Twitter + Telegram (PARALLEL) |

## Monitoring Dashboard

All dispatches are logged to:
- **Supabase** (OCI VM 92.5.60.87:8006) — dispatch_log table
- **GitHub Issues** — for failed dispatches
- **Telegram** — real-time alerts to operator

## Fleet Scaling

The dispatch engine scales linearly with the fleet size.
When a new A2A agent is created:
1. Add it to `fleet-registry.json`
2. The God Agent automatically discovers it on next request
3. No code changes needed — the registry IS the configuration
