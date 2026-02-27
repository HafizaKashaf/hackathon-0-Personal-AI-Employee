# Using Personal AI Employee with Qwen

This system is designed to work with **Qwen** as the AI reasoning engine instead of Claude Code.

## How It Works

The architecture remains the same - only the AI assistant changes:

| Component | Original (Claude) | Updated (Qwen) |
|-----------|------------------|----------------|
| Reasoning Engine | Claude Code | Qwen (via chat) |
| Trigger Method | CLI command | Chat prompt |
| Output | Terminal | Chat response |

## Workflow with Qwen

### Step 1: Run the Watcher

```bash
cd AI_Employee_Vault/scripts
python filesystem_watcher.py ..
```

This monitors the `Inbox/` folder and creates action files in `Needs_Action/`.

### Step 2: Run the Orchestrator (Qwen Mode)

```bash
cd AI_Employee_Vault/scripts
python orchestrator.py .. qwen
```

This will:
1. Check `Needs_Action/` for pending files
2. Write a prompt to `Updates/ai_prompt.txt`
3. Log what needs processing

### Step 3: Ask Qwen to Process

Copy the contents of `Updates/ai_prompt.txt` and ask Qwen:

> "I have files in my AI Employee vault's Needs_Action folder that need processing. Please:
> 1. Read the files in Needs_Action
> 2. Check Company_Handbook.md for rules
> 3. Create plans and process the items
> 4. Move completed items to Done folder
> 
> Here's the prompt from my orchestrator:
> [paste contents of ai_prompt.txt]"

Or simply share the vault context and ask:

> "Process all files in the Needs_Action folder of my AI Employee vault."

### Step 4: Qwen Executes

Qwen will:
1. Read the files in `Needs_Action/`
2. Create `Plans/Plan_*.md` for multi-step tasks
3. Create `Pending_Approval/` files for sensitive actions
4. Move completed items to `Done/`
5. Update `Dashboard.md`

## Commands Reference

### Watcher (No Changes)
```bash
python filesystem_watcher.py ..
```

### Orchestrator with Qwen
```bash
# Run once
python orchestrator.py .. qwen

# Continuous mode (check every 60 seconds)
python orchestrator.py .. qwen --continuous 60
```

### Orchestrator with Claude (Alternative)
```bash
python orchestrator.py .. claude
```

## File Structure for Qwen

```
AI_Employee_Vault/
├── Needs_Action/           # Files waiting for Qwen to process
├── Updates/
│   └── ai_prompt.txt       # Generated prompt (copy this to Qwen)
├── Plans/                  # Qwen creates plans here
├── Pending_Approval/       # Qwen creates approval requests here
├── Done/                   # Completed items moved here
└── Dashboard.md            # Updated by Qwen after processing
```

## Example Session

**Terminal:**
```bash
$ python orchestrator.py .. qwen
2026-02-26 16:30:00 - Orchestrator - INFO - Found 2 pending item(s)
2026-02-26 16:30:00 - Orchestrator - INFO - Prompt written to: Updates/ai_prompt.txt
```

**Then in Qwen chat:**
> "Process the files in my Needs_Action folder"

**Qwen responds:**
> "I'll process the files in Needs_Action. Let me start by reading them..."

**After Qwen finishes:**
- Check `Done/` for completed files
- Check `Dashboard.md` for updates
- Check `Pending_Approval/` for items needing your approval

## Tips

1. **Batch Processing**: Let files accumulate, then process them all at once
2. **Review Plans**: Check `Plans/` folder to see Qwen's thinking
3. **Approve Sensitive Actions**: Move files from `Pending_Approval/` to `Approved/` when ready
4. **Monitor Logs**: Check `Logs/` for activity history

---

*Qwen integration for Personal AI Employee - Bronze Tier*
