---
name: plan
description: "Ultimate plan-and-execute skill v2. 13 stages: Check, Research, Dependency Analysis, Plan Draft, Estimation & Risk, Critical Review, Quality Score, Approval & Decision Register, GitHub Sync, What-If Simulation, Execute, Auto Re-Plan, Verify, Post-Mortem & Learn. Adds: Plan JSON Schema, Dependency DAG, 3-Point Estimation (PERT), Monte Carlo, Risk Scoring (0-100), OKR Framework, Decision Register, Assumptions Log, Plan Quality Score (0-100), Auto Re-Plan Triggers, Plan Templates, Multi-Stage Approval, What-If Simulation, Post-Mortem Learning Loop, Blocker Detection, Plan Versioning, Continuous Planning Mode. Replaces /check-plan-done, /omoc-plan-swarm, /biometrics-plan."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: plan-and-execute
  trigger: plan
  version: 2.0
---

# /plan v2 - World-Class Plan & Execute Skill

> Check, Research, Analyze, Plan, Score, Review, Approve, Sync, Simulate, Execute, Verify, Learn

**Replaces:** `/check-plan-done`, `/omoc-plan-swarm`, `/biometrics-plan`
**Version:** 2.0 - World-Class Planning Features Integrated

---

## Purpose

One skill for everything planning-related. Modes:
- **plan-only:** Strategy, roadmap, architecture only
- **plan-and-execute:** Build, fix, implement, ship
- **resume-approved-plan:** Continue existing approved plan
- **continuous-planning:** Living plan with auto-adaptation

Incorporates best practices from Linear (Visual Initiatives), GitHub Projects (Code-Adjacent Roadmaps), Amazon Working Backwards (PR/FAQ), Netflix (Outcome-Driven), Stripe OKRs (Narrative 6-Pagers), GitLab Epics (Radical Transparency), Shopify (Async Anti-OKR), Notion (Database-Driven), Jira Advanced Roadmaps (Enterprise Portfolio).

---

## Trigger Words

`plan`, `plane`, `planung`, `planning`, `erstelle einen plan`, `create a plan`, `roadmap`, `strategy`, `strategie`, `konzept`, `blueprint`, `architektur`

---

## Design Principles

1. **Pipeline over Hierarchy** - sequential stages with clear I/O contracts
2. **Outcome over Output** - plans measured by business/user outcomes (OKRs), not task completion
3. **Data-Driven Estimation** - 3-point estimates with PERT formula, not gut feelings
4. **Dependency-Aware** - explicit DAG for critical path identification
5. **Quantified Risk** - numerical risk scores (0-100) with expected value
6. **Fail-Fast Gates** - check quality BEFORE passing to next stage
7. **Parallel Where Independent** - research runs parallel, rest sequential
8. **No Fictional Agents** - real OpenCode tools only
9. **Cost Guardrails** - bounded calls, no unbounded loops
10. **GitHub is Truth** - approved plans synced to GitHub Issues
11. **Continuous over Batch** - plans are living documents
12. **Decision Velocity** - how fast can we pivot on new data
13. **Learn from History** - every plan feeds accuracy back

---

## Modes

| Mode | When | Flow |
|------|------|------|
| `plan-only` | Strategy, roadmap, architecture | Stages 0 through 3.5, then stop |
| `plan-and-execute` | Build, fix, implement, ship | Full Stages 0 through 7 |
| `resume-approved-plan` | Existing approved plan matches | Skip to Stage 5 (Execute) |
| `continuous-planning` | Living plan with auto-adaptation | Full loop with monitor and auto-re-plan |

---

## Core Rules

- Real OpenCode tools only
- Bounded research: 2 parallel, 1 synthesis, 1 review
- Short single-purpose prompts
- Session context by default
- No fictional agents or undefined file dependencies
- No auto-commit in core loop
- Derive validation from actual stack
- Max 1 revision after critical review
- Continue until done criteria pass or real blocker
- **KING CEO TRACKING:** Git repo = sync to GitHub Issues before execution
- **OUTCOME FIRST:** Every plan defines measurable OKRs
- **DEPENDENCY DAG:** Every plan models task dependencies as DAG
- **RISK SCORE:** Every plan has quantified overall risk (0-100)
- **QUALITY SCORE:** Every plan must pass minimum 70/100
- **PLAN VERSIONING:** Every change creates new version with diff

---

## Architecture

```
STAGE 0:    CHECK - Existing approved plan?
STAGE 1:    RESEARCH (parallel) - Librarian + Explore
STAGE 1.5:  DEPENDENCY ANALYSIS - Build DAG, find critical path
STAGE 2:    PLAN DRAFT - Synthesize with OKRs, phases, tasks, deps, risks
STAGE 2.5:  ESTIMATION & RISK - PERT, Monte Carlo, risk scoring, rollback
STAGE 3:    CRITICAL REVIEW - Hard review by artistry agent
STAGE 3.2:  QUALITY SCORE - Auto-calculate 0-100
STAGE 3.5:  APPROVAL & DECISION REGISTER - Multi-stage, decision log, assumptions
STAGE 4:    SYNC - GitHub Project/Issue creation
STAGE 4.5:  WHAT-IF SIMULATION - Delay, resource, risk scenarios
STAGE 5:    EXECUTE - Task-by-task with validation
STAGE 5.5:  AUTO RE-PLAN - Triggered by slip, blocker, scope change
STAGE 6:    VERIFY - All done criteria + outcome measurement
STAGE 6.5:  POST-MORTEM & LEARNING - Accuracy metrics, retrospective, velocity update
STAGE 7:    CLOSEOUT - GitHub close, Wiki sync
```

---

## Plan JSON Schema v2

Every plan MUST conform to this schema:

```json
{
  "$schema": "https://opencode.ai/schemas/plan-v2.json",
  "version": "2.0.0",
  "id": "plan_YYYY-MM-DD_NNN",
  "title": "Plan Title",
  "mode": "plan-only|plan-and-execute|resume-approved-plan|continuous-planning",
  "created": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD",
  "version_number": 1,
  "status": "draft|approved|in-progress|completed|re-planned",

  "outcomes": {
    "objective": "What business/user outcome",
    "key_results": [
      {"metric": "metric name", "target": "target value", "current": "current value"}
    ]
  },

  "current_state": {
    "strengths": ["list"],
    "weaknesses": ["list"],
    "critical_gaps": ["list"]
  },

  "decisions": [
    {"decision": "what", "rationale": "why", "alternatives": ["list"], "owner": "role", "date": "YYYY-MM-DD"}
  ],

  "assumptions": [
    {"assumption": "what", "confidence": 0.95, "validation": "how to check"}
  ],

  "phases": [
    {
      "id": "P1",
      "name": "Phase Name",
      "priority": "critical|high|medium|optional",
      "tasks": [
        {
          "id": "P1-T1",
          "description": "What to do",
          "effort": {"pessimistic": "4h", "realistic": "2h", "optimistic": "1h"},
          "dependencies": ["P1-T0"],
          "validation": "How to verify",
          "owner": "role",
          "status": "not-started|in-progress|done|blocked"
        }
      ]
    }
  ],

  "dependency_graph": {
    "nodes": ["P1-T1", "P1-T2"],
    "edges": [{"from": "P1-T1", "to": "P1-T2", "type": "hard|soft|external"}],
    "critical_path": ["P1-T1", "P1-T2"]
  },

  "risks": [
    {
      "id": "R1",
      "description": "What could go wrong",
      "likelihood": 0.3,
      "impact": 8,
      "score": 24,
      "mitigation": "What to do about it",
      "owner": "role",
      "status": "identified|mitigated|occurred"
    }
  ],

  "overall_risk_score": 24,
  "plan_quality_score": 85,

  "rollback_plan": {
    "trigger": "What triggers rollback",
    "action": "What to do",
    "max_loss": "Worst case"
  },

  "done_criteria": [
    {"criterion": "Measurable outcome", "status": "not-met|met"}
  ],

  "approvals": [
    {"role": "tech-lead", "status": "pending|approved|rejected", "date": null}
  ],

  "metrics": {
    "planned_duration_hours": 40,
    "confidence_50": "35h",
    "confidence_85": "52h",
    "confidence_95": "68h",
    "scope_creep_count": 0,
    "replan_count": 0
  },

  "learning": {
    "planned_vs_actual": null,
    "accuracy_score": null,
    "retrospective": null
  }
}
```

---

## Stage 0: Check

Before planning, answer:

1. Is there already an approved plan in current session or task context?
2. Does that plan still match the current request?
3. Does it contain: outcomes (OKRs), concrete tasks, dependency DAG, risk scores, validation steps, done criteria?
4. Has the plan been synced to GitHub Issues?

If YES to all four, skip to Stage 5 in `resume-approved-plan` mode.
Otherwise, create fresh plan starting at Stage 1.

---

## Stage 1: Research (parallel)

Run both tasks in parallel with `run_in_background: true`.

### Task A: Librarian - Web and Docs Research

```
task({
  subagent_type: "librarian",
  run_in_background: true,
  load_skills: [],
  description: "Best-practice research for: [TOPIC]",
  prompt: `
Research this implementation topic. Focus on 2025-2026 sources.

TOPIC: [insert task description]
DATE: [today's date]

Deliver:
1. Current best practices with source URLs
2. Stable production-ready technology versions
3. Known anti-patterns to avoid
4. Community consensus from experts
5. Real-world case studies from top companies (Amazon, Linear, Stripe, GitHub, Netflix)
6. Tool recommendations with pros and cons

Output: concise markdown with concrete findings and sources.
No filler. Only verified, current information.
  `
})
```

### Task B: Explore - Codebase Analysis

```
task({
  subagent_type: "explore",
  run_in_background: true,
  load_skills: [],
  description: "Context analysis for: [TOPIC]",
  prompt: `
Analyze the local codebase or project context.

TASK: [insert task description]
PATH: [project path]

Deliver:
1. Project structure and tech stack (versions from lock files)
2. Existing patterns to preserve, code quality assessment
3. Dependencies: outdated, vulnerable, or unused
4. Integration points that could break during changes
5. Gaps: what is missing for production-readiness
6. Validation commands already used by the project
7. Implicit dependencies between services or modules
8. Circular dependency analysis if applicable

Output: concise markdown with file:line references.
  `
})
```

### Gate 1: Research Quality

Do not proceed unless:
- Librarian returned concrete findings with source URLs
- Explore returned file references and specific findings
- Both outputs contain 200+ words of substance
- Research identifies both good patterns AND failure risks
- Dependency analysis covers service, data, and team dependencies

If one branch is weak, re-run only that branch once with tighter prompt.
If both are weak, stop and report.

---

## Stage 1.5: Dependency Analysis

Build a Dependency DAG from research outputs:

1. Extract explicit and implicit dependencies from research
2. Classify: hard (blocking), soft (nice-to-have), external (third-party)
3. Map critical path: longest path through dependency graph
4. Identify blockers: tasks with no parallel execution path
5. Single points of failure: tasks blocking multiple downstream items
6. External dependencies: APIs, services, teams outside your control

Output: Mermaid diagram and JSON dependency graph in the plan.

---

## Stage 2: Draft Plan (sequential)

Synthesize one execution-ready plan from research outputs.

```
task({
  category: "deep",
  load_skills: [],
  run_in_background: false,
  description: "Create plan for: [TOPIC]",
  prompt: `
Create an execution-ready plan following Plan JSON Schema v2.

TASK: [insert task description]
BEST PRACTICES: [paste Librarian output]
LOCAL CONTEXT: [paste Explore output]

Use this EXACT structure:

# Plan: [Title]
Mode: [plan-only | plan-and-execute | resume-approved-plan | continuous-planning]
Created: [date] | Scope: [what] | Version: 1

## Outcomes (OKRs)
**Objective:** [what business or user outcome]
**Key Results:**
- KR1: [metric] from [current] to [target]
- KR2: [metric] from [current] to [target]

## Current State
[strengths, weaknesses, critical gaps]

## Decisions
| Decision | Rationale | Alternatives | Owner |
|----------|-----------|-------------|-------|

## Assumptions
| Assumption | Confidence | Validation Method |
|------------|-----------|-------------------|

## Phases

### Phase 1: [name] - CRITICAL
- [ ] P1-T1: [task] (P=4h/R=2h/O=1h, deps: [], validation: ...)
- [ ] P1-T2: [task] (P=/R=/O=, deps: [P1-T1], validation: ...)

### Phase 2: [name] - HIGH
- [ ] P2-T1: [task] (P=/R=/O=, deps: [P1-T2], validation: ...)

### Phase 3: [name] - OPTIONAL
- [ ] P3-T1: [task] (P=/R=/O=, deps: [P2-T1], validation: ...)

## Dependency Graph
[Mermaid diagram or text description]
Critical Path: P1-T1 -> P1-T2 -> P2-T1

## Risk Register
| ID | Risk | Likelihood (0-1) | Impact (1-10) | Score | Mitigation | Owner |
|----|------|-----------------|---------------|-------|------------|-------|
Overall Risk Score: [0-100]

## Rollback Plan
- Trigger: [what triggers rollback]
- Action: [what exactly to do]
- Max Loss: [worst-case time or data loss]

## Done Criteria
- [ ] [measurable outcome tied to OKR]
- [ ] [validation passes]
- [ ] [no regressions]

## Approval Gates
- [ ] Tech Lead
- [ ] Engineering Manager
- [ ] Product Owner (if user-facing)

RULES:
- Every task must be concrete and actionable
- Every task must include: 3-point estimate, dependencies, validation
- Effort estimates mandatory: Pessimistic, Realistic, Optimistic
- Phase 1 must be smallest critical path
- Maximum 3 phases
- Every risk needs likelihood (0-1), impact (1-10), score = likelihood times impact
- Overall risk score = sum of all risk scores, capped at 100
  `
})
```

### Gate 2: Plan Completeness

Do not proceed unless the plan includes:
- Outcomes or OKRs section with measurable key results
- Current state analysis
- Decisions table with rationale
- Assumptions table with confidence levels
- At least one phase with concrete tasks
- 3-point estimates (P/R/O) on every task
- Explicit dependencies per task
- Validation step per task
- Dependency graph
- Risk register with scores
- Overall risk score (0-100)
- Rollback plan
- Done criteria
- Approval gates

If sections are missing, fix the plan before review.

---

## Stage 2.5: Estimation and Risk Analysis

### 3-Point Estimation (PERT Formula)

For each task:
- Pessimistic (P): everything goes wrong
- Realistic (R): normal conditions
- Optimistic (O): everything goes right
- Expected (E) = (P + 4*R + O) / 6

### Monte Carlo Simulation (simplified)

```
total_pessimistic = sum(all P estimates)
total_realistic = sum(all R estimates)
total_optimistic = sum(all O estimates)
expected_total = (total_pessimistic + 4*total_realistic + total_optimistic) / 6
std_dev = (total_pessimistic - total_optimistic) / 6

confidence_50 = expected_total
confidence_85 = expected_total + std_dev
confidence_95 = expected_total + 2*std_dev
```

### Risk Scoring

```
risk_score = likelihood (0.0-1.0) times impact (1-10)
overall_risk = min(100, sum(all risk_scores))

Risk level:
0-20:   LOW - proceed with monitoring
21-40:  MEDIUM - proceed with mitigation
41-60:  HIGH - proceed only with approved mitigations
61-80:  CRITICAL - re-scope or add resources
81-100: BLOCKER - cannot proceed, must re-plan
```

### Gate 2b: Estimation Confidence

Do not proceed unless:
- All tasks have 3-point estimates
- Confidence 95th percentile is within 2x of expected total
- Overall risk score is 60 or below

---

## Stage 3: Critical Review (sequential)

One hard review. Be direct. No praise.

```
task({
  category: "artistry",
  load_skills: [],
  run_in_background: false,
  description: "Critical review of plan for: [TOPIC]",
  prompt: `
Review this plan critically. Be direct. No praise.

PLAN:
[paste plan from Stage 2]

Checklist:
1. OUTCOME ALIGNMENT - Do tasks directly achieve OKRs?
2. CRITICAL GAPS - What is missing that would cause failure?
3. FALSE ASSUMPTIONS - What does the plan assume without proof?
4. DEPENDENCY ERRORS - Are deps correct? Is critical path right?
5. ESTIMATION QUALITY - Are estimates realistic?
6. RISK COVERAGE - Are major risks identified? Scores realistic?
7. PRIORITY ERRORS - Is Phase 1 actually the critical path?
8. SCOPE - Realistic or overambitious?
9. TECH CHOICES - Sound for 2026?
10. NEW DEBT - Does this CREATE technical debt?
11. ROLLBACK ADEQUACY - If Phase 1 fails, is rollback sufficient?

Output format:

## Verdict: APPROVED or NEEDS REVISION

## Issues by severity
### CRITICAL
- ...
### HIGH
- ...
### LOW
- ...

## Suggested Changes
[Concrete rewrites, not vague advice]

RULES:
- If solid, say APPROVED with only minor improvements
- If CRITICAL issues, say NEEDS REVISION and be specific
- Never say "looks good overall"
  `
})
```

### Gate 3: Approval Readiness

| Verdict | Action |
|---------|--------|
| APPROVED, no CRITICAL | Continue to Stage 3.2 |
| NEEDS REVISION with CRITICAL | Integrate changes yourself, re-check, max 1 revision |
| Still critical after 1 revision | Stop, present with OPEN ISSUES |

---

## Stage 3.2: Plan Quality Score

Auto-calculate quality score (0-100):

| Category | Weight | Criteria |
|----------|--------|----------|
| Completeness | 25 | All sections present, OKRs defined, deps mapped |
| Clarity | 20 | Tasks unambiguous, validation clear, criteria measurable |
| Risk Coverage | 20 | Major risks identified, scores realistic, mitigations defined |
| Estimation Quality | 15 | 3-point estimates present, confidence intervals reasonable |
| Dependency Modeling | 10 | DAG correct, critical path identified, blockers flagged |
| Outcome Alignment | 10 | Every task maps to KR, OKRs measurable |

Quality Score formula:
(completeness divided by 100 times 25) + (clarity divided by 100 times 20) + (risk_coverage divided by 100 times 20) + (estimation_quality divided by 100 times 15) + (dependency_modeling divided by 100 times 10) + (outcome_alignment divided by 100 times 10)

### Gate 3b: Quality Threshold

- 85+: Excellent, proceed immediately
- 70-84: Good, proceed with noted improvements
- 50-69: Needs work, fix before review
- Below 50: Unacceptable, re-plan from scratch

---

## Stage 3.5: Multi-Stage Approval and Decision Register

### Approval Workflow

Tech Lead, then Engineering Manager, then Product Owner if user-facing.

```bash
gh issue create --title "[Approval] [Role] - Plan: <title>" \
  --body "<plan summary>" \
  --label "approval,plan:<title>" \
  --assignee <role-owner>
```

### Decision Register

| Decision | Rationale | Alternatives | Decided By | Date | Status |
|----------|-----------|-------------|------------|------|--------|

### Assumptions Log

| Assumption | Confidence | Validation | Status |
|------------|-----------|------------|--------|

If plan-only mode, return approved plan and stop.
If plan-and-execute mode, continue to Stage 4.

---

## Stage 4: Sync - GitHub Project and Issue Creation

### Option A: Issue Architect (Recommended)

```bash
node ~/dev/sin-solver-control-plane/packages/cli/src/index.mjs issues \
  --plan <path_to_plan.md> \
  --repo <owner/repo> \
  --phase <phase_id> \
  --dry-run
```

Remove --dry-run for real creation.

### Option B: Manual GitHub (Fallback)

```bash
gh issue create --title "[Master] <plan title>" \
  --body "<plan markdown>" --label "master-tracker,plan"
```

### Option C: Linear or Jira or Asana (if configured)

```bash
# Linear
linear-cli issue create --title "<title>" --label "plan" --estimate <points>

# Jira
jira create --project <key> --issuetype Epic --summary "<title>"
```

Output the created tracker URL.

---

## Stage 4.5: What-If Simulation

Run 2-3 scenarios before execution:

```
task({
  category: "deep",
  load_skills: [],
  run_in_background: false,
  description: "What-if simulation for plan",
  prompt: `
Simulate these scenarios:

PLAN: [paste plan]

SCENARIOS:
1. DELAY: What if critical path task takes 2x longer?
2. RESOURCE: What if we add one more developer?
3. RISK: What if Risk R1 materializes?

For each: new completion date, affected tasks, recommended mitigation, whether re-planning is needed.

Output: scenario analysis table with pass or fail verdict.
  `
})
```

---

## Stage 5: Execute

Turn approved plan into live task loop.

Execution rules:
- One concrete task at a time
- Keep aligned with approved phase order
- Run exact validation after each task
- Mark done ONLY after validation passes
- Live Tracker Update: `gh issue comment <ID> --body "Done: <details>"`
- Burndown Tracking: update remaining effort after each task
- Fix validation failures before moving on
- One focused background consultation if truly blocked
- Do NOT claim success while done criteria are open
- No unbounded orchestration loop

---

## Stage 5.5: Automated Re-Plan Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Schedule Slip | Actual over 120% of planned | Re-estimate remaining |
| Blocker Detected | Task blocked over 24h | Re-scope or escalate |
| Scope Creep | More than 2 new requirements | Re-plan with new scope |
| Risk Materialized | Any risk status = occurred | Activate mitigation, re-plan if needed |
| Resource Change | Team size changes | Re-estimate with new capacity |
| Dependency Failure | External dependency unavailable | Find alternative or re-plan |

When re-plan triggered:
1. Log re-plan event with reason
2. Jump to Stage 2
3. Keep previous learnings and decisions
4. Increment plan version number
5. Re-run review (Stage 3) and quality score (Stage 3.2)

---

## Stage 6: Verify Done

Before stopping:
- Every required task completed or explicitly deferred with reason
- Every done criterion passes
- All critical validations passed
- Remaining risks or open issues stated clearly
- Tracker Closeout: close GitHub sub-tasks and master epic with final summary
- Outcome Verification: Key Results measured and compared to targets

Return:
- What was completed
- What was validated
- What remains open
- Plan accuracy metrics (planned vs actual)

If work is not done, continue the loop.

---

## Stage 6.5: Post-Mortem and Learning Loop

### Plan Accuracy Metrics

```
accuracy_score = 1 - |actual_duration - planned_duration| / planned_duration
per_task_accuracy = average(1 - |actual_i - planned_i| / planned_i for each task i)
scope_creep_rate = new_tasks_added / original_task_count
replan_rate = replan_count / total_plans
```

### Retrospective Template

```bash
gh issue comment <MASTER_ID> --body "
## Retrospective

### What Went Well
- [items]

### What Could Be Better
- [items]

### Plan Accuracy
- Planned: X hours, Actual: Y hours, Accuracy: Z%
- Tasks on time: N/M
- Scope changes: K
- Re-plans: R

### Learnings for Future Plans
- [specific insight]
- [estimation adjustment]
- [process improvement]
"
```

### Velocity Baseline Update

Store actual durations for future estimation:
```
velocity_db[task_type] = {
  avg_duration: ...,
  std_dev: ...,
  sample_count: ...,
  last_updated: ...
}
```

---

## Stage 7: Closeout

### Issue Board Closeout

```bash
gh issue close <ID> --comment "Completed: <summary>"

gh issue close <EPIC_ID> --comment "
## Final Status
Completed: X/Y tasks
Validated: <results>
Plan Accuracy: Z%
Open issues: <none or list>
"
```

### Wiki Documentation Sync

If the project has a GitHub Wiki:
1. Run `~/.config/opencode/scripts/sync-github-wiki.sh <plan_path>`
2. If script reports "WIKI NOT INITIALIZED", use browser automation to create initial page, then re-run.

---

## Anti-Patterns To Reject

| Anti-Pattern | Why | Replacement |
|-------------|-----|-------------|
| Vague quality claims | Not measurable | Concrete gates with pass/fail |
| Hidden dependencies | Brittle | Explicit dependency DAG |
| Story points | Abstract, gameable | PERT 3-point estimation with historical data |
| Static risk matrix | Outdated instantly | Real-time RAG from CI/CD health, bugs, scope creep |
| Annual batch planning | Too slow for 2026 | Continuous planning with decision velocity |
| Planning without outcomes | Tasks for tasks sake | OKR-first, outcome-driven planning |
| Fictional agent names | No real tool mapping | Real task() with subagent_type or category |
| Mandatory auto-commit | Unsafe, destructive | Explicit commit only when user requests |
| Planning without review | Blind spots | Stage 3 critical review mandatory |
| Execution without done criteria | Cannot verify | Every plan MUST have done criteria |
| Infinite loops | Resource waste | Bounded loops with stop conditions |
| Premature success | User loses trust | Verify ALL done criteria before stopping |
| Plans without rollback | No safety net | Every plan needs rollback trigger and action |
| Plans without versioning | Cannot track changes | Every change increments version with diff |
| Subjective project health | PM gut feeling | Algorithmic RAG from pipeline, bugs, scope |
| Output metrics over outcomes | Revenue targets miss quality | Controllable Input Metrics (Amazon style) |

---

## Cost Awareness

| Stage | Calls | Latency | Notes |
|-------|-------|---------|-------|
| Research | 2 parallel | 1 LLM round | Librarian + Explore simultaneously |
| Plan Draft | 1 sequential | 1 LLM round | Synthesizes research |
| Review | 1 sequential | 1 LLM round | Critical review |
| Simulation | 0-1 sequential | 0-1 LLM rounds | Optional what-if |
| **Total Planning** | **4-5 calls** | **4-5 LLM rounds** | vs 6+ in old designs |

- Re-run only weak research branch, not both
- Max 1 revision round after review
- Results stay in session context, no temp files

---

## Tool Reference

| Stage | Tool | Purpose |
|-------|------|---------|
| Research | task(subagent_type: librarian) | Web and docs research |
| Research | task(subagent_type: explore) | Codebase analysis |
| Plan | task(category: deep) | Synthesize plan |
| Review | task(category: artistry) | Critical review |
| Simulation | task(category: deep) | What-if scenarios |
| Sync | gh issue create or Issue Architect CLI | Persist to GitHub |
| Execute | gh issue comment | Live tracker updates |
| Closeout | gh issue close | Issue board closeout |

---

## Plan Templates

Use these templates for common scenarios. Load the template, fill in specifics.

### Feature Build Template
- Phase 1: API and data model (critical path)
- Phase 2: UI and integration
- Phase 3: Polish and edge cases (optional)

### Bug Fix Template
- Phase 1: Reproduce and root cause (critical)
- Phase 2: Fix and regression tests
- Phase 3: Monitor in production (optional)

### Migration Template
- Phase 1: Build parallel system (critical)
- Phase 2: Dual-write and verify
- Phase 3: Cutover and cleanup

### Refactor Template
- Phase 1: Add tests around current behavior (critical)
- Phase 2: Incremental refactoring
- Phase 3: Remove old code

---

## Practical Summary

1. Check whether usable approved plan exists
2. Research with bounded parallel tasks (Librarian + Explore)
3. Analyze dependencies and build DAG
4. Plan with OKRs, 3-point estimates, risk scoring
5. Score quality (minimum 70/100)
6. Review with hard critique gate
7. Approve with decision register
8. Sync to GitHub Issues
9. Simulate what-if scenarios
10. Execute task by task with validation
11. Auto-re-plan on slip, blocker, scope change
12. Verify all done criteria and measure outcomes
13. Post-mortem: accuracy metrics, retrospective, velocity update
14. Closeout: GitHub close, Wiki sync

That is what /plan v2 means. World-class planning. One skill.
