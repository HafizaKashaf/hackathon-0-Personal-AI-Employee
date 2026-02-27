# Personal AI Employee - Bronze Tier

A local-first, autonomous AI employee that manages your personal and business affairs using **Qwen** (or Claude Code) and **Obsidian**.

## 🏆 Bronze Tier Deliverables (Complete ✅)

- ✅ **Obsidian vault** with Dashboard.md, Company_Handbook.md, and Business_Goals.md
- ✅ **File System Watcher** - monitors Inbox folder for new files
- ✅ **Orchestrator** - triggers AI (Qwen/Claude) to process pending items
- ✅ **Basic folder structure**: /Inbox, /Needs_Action, /Done, /Plans, etc.
- ✅ **AI integration** - reads from and writes to the vault
- ✅ **Live demonstration** - files processed successfully!

## ✅ Live Demo Results

The Bronze Tier workflow has been **successfully tested with Qwen**:

| Folder | Before | After |
|--------|--------|-------|
| `Needs_Action/` | 2 files | 0 files (processed) |
| `Done/` | 0 files | 3 files (completed) |
| `Plans/` | 0 files | 1 plan (completed) |
| `Pending_Approval/` | 0 files | 0 files (no approval needed) |
| `Accounting/` | 0 files | 1 invoice log |
| `Invoices/` | 0 files | 1 invoice copied |
| `Dashboard.md` | Old stats | Updated with activity |

### What Qwen Did:

1. **Read** files in `Needs_Action/` (test file + invoice)
2. **Created** `Plans/Plan_2026-02-26_process_files.md`
3. **Logged** invoice to `Accounting/Invoice_Log_2026-02.md`
4. **Copied** invoice to `Invoices/` folder
5. **Moved** completed files to `Done/`
6. **Updated** `Dashboard.md` with new stats
7. **Logged** all actions to `Logs/2026-02-26.jsonl`

## 📁 Project Structure

```
hackathon-0-Personal-AI-Employee/
├── AI_Employee_Vault/          # Obsidian vault (your AI's memory)
│   ├── Dashboard.md            # Real-time summary dashboard
│   ├── Company_Handbook.md     # Rules of engagement
│   ├── Business_Goals.md       # Your objectives
│   ├── USING_WITH_QWEN.md      # Qwen-specific instructions
│   ├── Inbox/                  # Drop files here for processing
│   ├── Needs_Action/           # Items awaiting processing
│   ├── Done/                   # Completed tasks
│   ├── Plans/                  # Multi-step plans
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved for execution
│   ├── Logs/                   # Activity logs
│   ├── Briefings/              # CEO briefings (weekly reports)
│   ├── Accounting/             # Financial records
│   ├── Invoices/               # Generated invoices
│   └── scripts/                # Python scripts
│       ├── base_watcher.py     # Abstract watcher base class
│       ├── filesystem_watcher.py # File system monitor
│       └── orchestrator.py     # AI trigger (Qwen/Claude)
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.13+** - [Download](https://www.python.org/downloads/)
2. **Qwen** (this chat interface) - Already using!
3. **Obsidian** (optional, for viewing vault) - [Download](https://obsidian.md/download)

### Step 1: Start the File System Watcher

Open a terminal and run:

```bash
cd AI_Employee_Vault/scripts
python filesystem_watcher.py ..
```

This watches the `Inbox/` folder. Leave this running in the background.

### Step 2: Run the Orchestrator (Qwen Mode)

In another terminal:

```bash
cd AI_Employee_Vault/scripts
python orchestrator.py .. qwen
```

This will:
1. Check `Needs_Action/` for pending items
2. Write a prompt to `Updates/ai_prompt.txt`
3. You then ask Qwen to process the files

### Step 3: Ask Qwen to Process

Tell Qwen:

> "Process all files in the Needs_Action folder of my AI Employee vault."

Or for continuous mode:

```bash
python orchestrator.py .. qwen --continuous 60
```

## ⚙️ How It Works

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  File Drop      │────▶│  File Watcher    │────▶│  Needs_Action/  │
│  (Inbox/)       │     │  (Python)        │     │  (Action Files) │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐     ┌────────▼────────┐
│  Dashboard.md   │◀────│  Qwen (AI)       │◀────│  Orchestrator  │
│  (Updated)      │     │  (Processing)    │     │  (Trigger)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### The Watcher Pattern

1. **Check** - Polls Inbox folder every 30 seconds
2. **Detect** - Identifies new files (by hash)
3. **Copy** - Duplicates to Needs_Action folder
4. **Create** - Generates `.meta.md` action file

### The Orchestrator Pattern (Qwen Mode)

1. **Scan** - Checks Needs_Action for `.md` files
2. **Update** - Refreshes Dashboard.md stats
3. **Write Prompt** - Creates `Updates/ai_prompt.txt`
4. **Qwen Processes** - You ask Qwen to execute
5. **Log** - Records all actions

## 📝 Configuration

### Adjust Watcher Interval

```python
# In filesystem_watcher.py
watcher = FileSystemWatcher(vault_path, check_interval=30)  # Change 30 to desired seconds
```

### Adjust Orchestrator Interval

```bash
# Command line
python orchestrator.py .. qwen --continuous 60  # Check every 60 seconds
```

## 📝 Logs

All activity is logged to `AI_Employee_Vault/Logs/`:

- `watcher_YYYY-MM-DD.log` - File detection events
- `orchestrator_YYYY-MM-DD.log` - Processing cycles
- `YYYY-MM-DD.jsonl` - Structured action logs

## 🎯 Next Steps (Silver Tier)

After Bronze Tier is working reliably:

1. **Gmail Watcher** - Monitor Gmail for important emails
2. **WhatsApp Watcher** - Detect urgent messages (uses Playwright)
3. **MCP Servers** - Enable external actions (send email, make payments)
4. **HITL Workflow** - Human approval for sensitive actions
5. **Scheduled Tasks** - cron/Task Scheduler integration

## 🐛 Troubleshooting

### Watcher not detecting files?

- Check that files are in `Inbox/` (not subfolders)
- Verify the watcher is running (check Logs/)
- Ensure no other process has locked the files

### Permission errors?

Ensure the vault folder has read/write permissions. On Windows, run terminal as Administrator if needed.

### Encoding errors on Windows?

All files use UTF-8 encoding. If you see encoding errors:

```bash
chcp 65001  # Set console to UTF-8
```

## 📚 Documentation

- [AI_Employee_Vault/README.md](AI_Employee_Vault/README.md) - Detailed vault usage
- [AI_Employee_Vault/USING_WITH_QWEN.md](AI_Employee_Vault/USING_WITH_QWEN.md) - Qwen-specific guide
- [AI_Employee_Vault/Company_Handbook.md](AI_Employee_Vault/Company_Handbook.md) - AI rules and guidelines
- [QWEN.md](QWEN.md) - Project architecture overview

## 📅 Wednesday Research Meetings

Join the community building sessions:

- **When**: Wednesdays at 10:00 PM PKT
- **First Meeting**: January 7th, 2026
- **Zoom**: [Join Link](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **YouTube**: [@panaversity](https://www.youtube.com/@panaversity)

## 🏅 Bronze Tier Checklist

- [x] Obsidian vault created with required folders
- [x] Dashboard.md with real-time stats
- [x] Company_Handbook.md with rules
- [x] Business_Goals.md template
- [x] File System Watcher working
- [x] Orchestrator triggering AI
- [x] Sample test files created
- [x] Logs being generated
- [x] Dashboard updating correctly
- [x] **Live demo: Qwen processed files successfully**

---

*Built for the Personal AI Employee Hackathon 0 - Building Autonomous FTEs in 2026*

**AI Engine:** Qwen (with Claude Code support as alternative)
