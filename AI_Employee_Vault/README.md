# AI Employee Vault - Bronze Tier

This is your Personal AI Employee's Obsidian vault. It serves as the memory, dashboard, and working directory for your AI Employee.

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Main dashboard - real-time summary
├── Company_Handbook.md       # Rules of engagement for the AI
├── Business_Goals.md         # Your business objectives and metrics
├── Inbox/                    # Drop files here for processing
├── Needs_Action/             # Items awaiting processing
├── Plans/                    # Multi-step task plans (created by AI)
├── Pending_Approval/         # Actions awaiting human approval
├── Approved/                 # Approved actions ready for execution
├── Done/                     # Completed tasks
├── Logs/                     # Activity logs
├── Briefings/                # CEO briefings (weekly reports)
├── Accounting/               # Financial records
├── Invoices/                 # Generated invoices
└── Updates/                  # Sync updates (for future tiers)
```

## Quick Start

### 1. Start the File System Watcher

```bash
cd scripts
python filesystem_watcher.py ..
```

This watches the `Inbox/` folder for new files.

### 2. Run the Orchestrator

```bash
cd scripts
python orchestrator.py ..
```

This checks `Needs_Action/` for pending items and triggers Claude Code.

### 3. Process with Claude Code

When the orchestrator triggers Claude, it will:
1. Read files in `Needs_Action/`
2. Check `Company_Handbook.md` for rules
3. Create plans and execute actions
4. Move completed items to `Done/`

### Manual Claude Code Usage

```bash
cd AI_Employee_Vault
claude "Process all files in Needs_Action folder"
```

## Testing the Bronze Tier

1. **Drop a file in Inbox/**
   - Any file you want processed
   
2. **Wait for the watcher** (30 second intervals)
   - Or run manually: `python filesystem_watcher.py ..`

3. **Check Needs_Action/**
   - Watcher creates `.meta.md` files here

4. **Run the orchestrator**
   - `python orchestrator.py .. --continuous` for continuous mode

5. **Verify Dashboard.md updates**

## Configuration

### Watcher Settings

Edit `filesystem_watcher.py`:
- `check_interval`: How often to check for new files (default: 30s)

### Orchestrator Settings

Edit `orchestrator.py`:
- `check_interval`: How often to check for pending items (default: 60s)

## Logs

All activity is logged to `Logs/` folder:
- `watcher_YYYY-MM-DD.log` - File watcher activity
- `orchestrator_YYYY-MM-DD.log` - Processing activity
- `YYYY-MM-DD.jsonl` - Structured action logs

## Next Steps (Silver Tier)

After Bronze Tier is working:
1. Add Gmail Watcher (requires Google API setup)
2. Add WhatsApp Watcher (requires Playwright)
3. Set up MCP servers for external actions
4. Implement human-in-the-loop approval workflow
5. Add scheduled tasks (cron/Task Scheduler)

## Troubleshooting

**Watcher not detecting files?**
- Check the Inbox folder path
- Ensure files are not hidden/system files
- Check logs in `Logs/` folder

**Claude Code not found?**
- Install: `npm install -g @anthropic/claude-code`
- Verify: `claude --version`

**Permission errors?**
- Ensure the vault folder has read/write permissions
- Run scripts with appropriate user privileges
