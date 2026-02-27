# Personal AI Employee Hackathon

## Project Overview

This is a hackathon project for building a **"Digital FTE" (Full-Time Equivalent)** - an autonomous AI agent that manages personal and business affairs 24/7. The system uses **Claude Code** as the reasoning engine and **Obsidian** as the local-first dashboard/memory.

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Claude Code | Reasoning engine, task planning, execution |
| **Memory/GUI** | Obsidian | Local Markdown vault for dashboard, tasks, audit logs |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems for triggers |
| **Hands** | MCP Servers | Model Context Protocol for external actions (email, browser, payments) |

### Key Design Principles

- **Local-first**: All data stored locally in Obsidian vault
- **Agent-driven**: Autonomous operation via watchers + reasoning loop
- **Human-in-the-loop**: Sensitive actions require approval before execution
- **Ralph Wiggum Pattern**: Stop hook keeps Claude iterating until tasks complete

## Directory Structure

```
hackathon-0-Personal-AI-Employee/
├── .qwen/skills/           # Qwen skills (browsing-with-playwright)
├── .claude/                # Claude Code configuration (plugins, MCP)
├── QWEN.md                 # This file - project context
├── skills-lock.json        # Skill dependencies lock file
└── *.md                    # Hackathon documentation
```

### Expected Obsidian Vault Structure (created during implementation)

```
AI_Employee_Vault/
├── Dashboard.md            # Real-time summary (bank, tasks, messages)
├── Company_Handbook.md     # Rules of engagement
├── Business_Goals.md       # Q1/Q2 objectives, metrics
├── Inbox/                  # Raw incoming items
├── Needs_Action/           # Items requiring processing
├── In_Progress/<agent>/    # Claimed tasks (prevents double-work)
├── Pending_Approval/       # HITL approval requests
├── Approved/               # Approved actions ready for execution
├── Done/                   # Completed tasks
├── Plans/                  # Multi-step task plans (Plan.md)
├── Accounting/             # Bank transactions, invoices
└── Briefings/              # CEO briefings (weekly audits)
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts, orchestration |
| Node.js | v24+ LTS | MCP servers |
| GitHub Desktop | Latest | Version control |

### Setup Commands

```bash
# Verify Claude Code installation
claude --version

# Start a watcher script (example)
python watchers/gmail_watcher.py

# Start Ralph Wiggum loop for autonomous task completion
/ralph-loop "Process all files in /Needs_Action" --max-iterations 10
```

### MCP Server Configuration

Configure in `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": { "GMAIL_CREDENTIALS": "/path/to/credentials.json" }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": { "HEADLESS": "true" }
    }
  ]
}
```

## Development Conventions

### Watcher Pattern

All watcher scripts follow the `BaseWatcher` abstract class:

```python
class BaseWatcher(ABC):
    def check_for_updates() -> list:      # Return new items to process
    def create_action_file(item) -> Path: # Create .md in Needs_Action
    def run():                            # Main loop with check_interval
```

### Action File Schema

```markdown
---
type: email|whatsapp|file_drop|approval_request
from/sender: <source>
subject: <topic>
priority: high|medium|low
status: pending|in_progress|done
created: <ISO timestamp>
---

## Content
<extracted content>

## Suggested Actions
- [ ] Action 1
- [ ] Action 2
```

### Approval Request Schema (HITL)

```markdown
---
type: approval_request
action: payment|send_email|post_social
amount: 500.00
recipient: <target>
created: <ISO timestamp>
expires: <ISO timestamp + 24h>
status: pending
---

## Details
<action details>

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

### Task Completion Patterns

1. **Promise-based**: Claude outputs `<promise>TASK_COMPLETE</promise>`
2. **File movement**: Task file moved from `Needs_Action/` → `Done/`

## Testing Practices

- Test watchers individually before integrating
- Use mock data in `/Inbox` for Claude reasoning tests
- Verify MCP servers in isolation before HITL workflow
- Log all actions to `/Briefings/` for audit trails

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12h | Obsidian vault, 1 watcher, Claude read/write |
| **Silver** | 20-30h | 2+ watchers, Plan.md, 1 MCP server, HITL workflow |
| **Gold** | 40+h | Full integration, Odoo MCP, weekly audit, Ralph loop |
| **Platinum** | 60+h | Cloud deployment, domain specialization, A2A upgrade |

## Key Resources

- [Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum)
- [Agent Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [MCP Server Reference](https://github.com/AlanOgic/mcp-odoo-adv)
- [Playwright Tools](./.qwen/skills/browsing-with-playwright/references/playwright-tools.md)

## Wednesday Research Meetings

- **When**: Wednesdays at 10:00 PM PKT
- **First Meeting**: January 7th, 2026
- **Zoom**: [Join Link](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **YouTube**: [@panaversity](https://www.youtube.com/@panaversity)
