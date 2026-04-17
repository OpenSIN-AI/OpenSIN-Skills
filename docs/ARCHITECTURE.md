# OpenSIN-Skills Architecture

## System Overview

```mermaid
flowchart LR
    subgraph Input
        USER[User Request]
    end

    subgraph "Skill Selection"
        TRIGGER[Proactive Triggers]
        CATALOG[catalog.json]
    end

    subgraph "Skill Library"
        KNOW[Knowledge Skills<br/>235 expertise skills]
        ACT[Action Skills<br/>47 operational skills]
    end

    subgraph "Execution"
        PERSONA[Persona Layer]
        ORCH[Orchestration]
        A2A[A2A Fleet]
        MCP[MCP Tools]
    end

    USER --> TRIGGER
    TRIGGER --> CATALOG
    CATALOG --> KNOW
    CATALOG --> ACT
    KNOW --> PERSONA
    ACT --> PERSONA
    PERSONA --> ORCH
    ORCH --> A2A
    ORCH --> MCP
```

## Skill Categories

### Knowledge Layer (claude-skills upstream)
Expertise skills that teach AI agents HOW TO THINK about domain problems.
Imported from [claude-skills](https://github.com/alirezarezvani/claude-skills) by Alireza Rezvani.

### Action Layer (OpenSIN native)
Operational skills that give AI agents the power to EXECUTE real-world tasks:
agent creation, browser automation, deployment, media generation, planning.

### Persona Layer
Role-based identities that combine multiple skills into coherent expert personalities.

### Orchestration Layer
Patterns for coordinating multiple skills and agents on complex tasks.

## Integration Points

- **OpenCode CLI**: Primary skill loading mechanism
- **A2A Agents**: Skill-powered autonomous agents
- **MCP Servers**: Tool exposure via Model Context Protocol
- **Fleet Dispatch**: Delegating work to HF VM coders via SIN-Hermes
