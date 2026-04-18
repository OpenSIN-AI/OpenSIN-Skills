# OpenSIN Orchestration Patterns

> Based on orchestration patterns from [claude-skills](https://github.com/alirezarezvani/claude-skills)
> by Alireza Rezvani (MIT License). Extended with 5 OpenSIN-native patterns.

## 9 Orchestration Patterns

### Imported Patterns (from claude-skills)

#### 1. Sequential Chain
Execute skills one after another, passing output as input to the next.
Best for: Linear workflows with clear dependencies.

```
Skill A → output → Skill B → output → Skill C → final result
```

#### 2. Parallel Fan-Out
Execute multiple skills simultaneously, then merge results.
Best for: Independent analyses that need to be combined.

```
         ┌→ Skill A →┐
Input →  ├→ Skill B →┤  → Merge → Result
         └→ Skill C →┘
```

#### 3. Expert Panel
Multiple skills review the same input from different perspectives.
Best for: Complex decisions requiring multi-disciplinary input.

```
         ┌→ Engineering Review  →┐
Input →  ├→ Product Review      →┤  → Synthesize → Decision
         └→ Business Review     →┘
```

#### 4. Iterative Refinement
One skill produces output, another reviews it, repeat until quality threshold met.
Best for: Content creation, code writing, document drafting.

```
Create → Review → Refine → Review → Approve
  ↑                 ↓
  └─── if rejected ─┘
```

### OpenSIN-Native Patterns

#### 5. Fleet Dispatch
Distribute work across multiple HF VM coders via SIN-Hermes.
Best for: Large-scale parallel coding tasks.

```
Zeus (Planner) → GitHub Issues → Hermes (Dispatcher) → HF VM Coders
                                                        ↓
                                                     PRs → Review → Merge
```

#### 6. A2A Chain
Chain multiple A2A agents, each specialized in one domain.
Best for: Cross-domain automation (e.g., research → code → deploy → notify).

```
SIN-Research → SIN-Coder → SIN-Deploy → SIN-Telegram (notify)
```

#### 7. Vision-Gated Browser Flow
Browser automation with mandatory vision verification between every action.
Best for: Survey filling, form automation, web scraping with verification.

```
Action → Screenshot → Vision Model → PROCEED? → Next Action
                                   → STOP?    → Report & Retry
```

#### 8. Self-Healing Loop
Agent detects failure, creates GitHub Issue, dispatches fix to fleet.
Best for: Autonomous error recovery and system resilience.

```
Agent Error → Log → GitHub Issue → Hermes Dispatch → Fleet Fix → Verify → Close Issue
```

#### 9. God Agent (SIN-Orchestrator) ⚡ NEW
Single entry point receives ANY request, classifies intent, selects agents from
the fleet registry, dispatches them ALL in parallel, and synthesizes results.
The user interacts with one agent. The fleet does the work.
Best for: EVERYTHING. This is the default pattern for all user interactions.

```
                         ┌→ Agent A (domain 1, bg) →┐
User → God Agent →  ├→ Agent B (domain 2, bg) →┤ → Synthesize → User
   (single chat)         ├→ Agent C (domain 3, bg) →┤   (single answer)
                         ├→ Agent D (domain 1, bg) →┤
                         └→ Agent E (domain 4, bg) →┘
```

Key properties:
- **126 agents** available for dispatch
- **17 Team Managers** for domain coordination
- **280+ skills** as knowledge augmentation
- **Zero human intervention** — never asks, always acts
- **Self-healing** — failures trigger automatic recovery
- **Skill-augmented** — every dispatch includes relevant skill content

## Usage

Select the appropriate pattern based on your task:

| Task Type | Recommended Pattern |
|-----------|-------------------|
| Any user request (DEFAULT) | **God Agent** (Pattern 9) |
| Step-by-step workflow | Sequential Chain |
| Independent analyses | Parallel Fan-Out |
| Complex decisions | Expert Panel |
| Content creation | Iterative Refinement |
| Large coding tasks | Fleet Dispatch |
| Cross-domain automation | A2A Chain |
| Browser automation | Vision-Gated Browser Flow |
| Error recovery | Self-Healing Loop |

## Integration

The God Agent (Pattern 9) can use ALL other patterns internally:
- Uses **Parallel Fan-Out** for multi-domain requests
- Uses **Sequential Chain** for dependent tasks
- Uses **Expert Panel** for complex decisions
- Uses **Fleet Dispatch** for large coding projects
- Uses **Self-Healing Loop** for failure recovery
- Uses **Vision-Gated Browser Flow** for web automation tasks

See `SIN-Orchestrator/SKILL.md` for the complete God Agent specification.
See `fleet-registry.json` for the machine-readable agent catalog.
See `AUTO-DISPATCH.md` for the parallel dispatch protocol.
See `skill-router.py` for the local routing engine.
