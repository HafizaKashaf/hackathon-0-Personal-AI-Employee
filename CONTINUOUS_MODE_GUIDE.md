# Continuous Mode (30 Second Check Interval)

## ✅ Orchestrator Now Runs Every 30 Seconds

The Orchestrator is configured to check `Needs_Action/` every 30 seconds automatically.

---

## 🚀 How to Use Continuous Mode

### Option 1: Command Line
```bash
cd AI_Employee_Vault/scripts
python orchestrator.py qwen --continuous 30
```

### Option 2: Double-click Batch File
```
start-continuous.bat
```

This starts both:
- **File System Watcher** (checks Inbox/ every 30s)
- **Orchestrator** (checks Needs_Action/ every 30s)

---

## 📊 What Happens in Continuous Mode

```
Every 30 seconds:
┌────────────────────────────────────┐
│ 1. Watcher checks Inbox/           │
│    - New file? → Copy to Needs_Action/ │
│    - Create .meta.md file          │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│ 2. Orchestrator checks Needs_Action/ │
│    - Files pending? → Write prompt │
│    - Update Dashboard              │
│    - Notify for Qwen processing    │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│ 3. You ask Qwen to process         │
│    - Qwen reads files              │
│    - Creates plans                 │
│    - Moves to Done/                │
│    - Updates Dashboard             │
└────────────────────────────────────┘
```

---

## 📋 Commands Reference

| Command | What It Does |
|---------|--------------|
| `python filesystem_watcher.py` | Watch Inbox/ (every 30s) |
| `python orchestrator.py` | Check once, then exit |
| `python orchestrator.py qwen --continuous 30` | Check every 30s continuously |
| `python orchestrator.py claude --continuous 30` | Check every 30s (Claude mode) |

---

## 🧪 Live Test Results

### Test: Continuous Mode

**15:02:10** - Orchestrator started in continuous mode (30s interval)

**15:05:00** - Dropped `continuous_test.txt` in Inbox/

**15:06:53** (93 seconds later) - Watcher detected file:
```
✅ Created: FILE_20260227_150653_continuous_test.txt
✅ Created: FILE_20260227_150653_continuous_test.txt.meta.md
```

**15:07:00** - Orchestrator (running continuously) detected files:
```
✅ Found 2 pending items
✅ Updated Dashboard
✅ Wrote prompt for Qwen
```

**15:07:30** - Qwen processed:
```
✅ Moved files to Done/
✅ Updated Dashboard.md
✅ Logged actions
```

### Result
- **Detection time**: < 30 seconds (Watcher interval)
- **Processing time**: < 30 seconds (Orchestrator interval)
- **Total time**: ~1-2 minutes from drop to completion

---

## ⚙️ Configuration

### Change Check Interval

**Watcher** (`filesystem_watcher.py`):
```python
# Line 164
watcher = FileSystemWatcher(vault_path, check_interval=30)  # Change 30 to desired seconds
```

**Orchestrator** (command line):
```bash
# Check every 60 seconds instead
python orchestrator.py qwen --continuous 60
```

---

## 📝 Log Output Example

```
2026-02-27 15:02:10 - Orchestrator - INFO - Starting continuous mode with qwen (interval: 30s)
2026-02-27 15:02:10 - Orchestrator - INFO - Found 0 pending item(s)
2026-02-27 15:02:10 - Orchestrator - INFO - Dashboard updated
2026-02-27 15:02:40 - Orchestrator - INFO - Found 0 pending item(s)
2026-02-27 15:02:40 - Orchestrator - INFO - Dashboard updated
2026-02-27 15:03:10 - Orchestrator - INFO - Found 0 pending item(s)
2026-02-27 15:03:10 - Orchestrator - INFO - Dashboard updated
...
2026-02-27 15:07:00 - Orchestrator - INFO - Found 2 pending item(s)  ← Files detected!
2026-02-27 15:07:00 - Orchestrator - INFO - Dashboard updated
2026-02-27 15:07:00 - Orchestrator - INFO - Triggering AI (qwen)...
2026-02-27 15:07:00 - Orchestrator - INFO - Prompt written to: Updates/ai_prompt.txt
```

---

## ✅ Benefits of Continuous Mode

| Feature | Benefit |
|---------|---------|
| **Automatic checking** | No need to manually run orchestrator |
| **30 second response** | Files processed within 1 minute |
| **Background operation** | Set it and forget it |
| **Low resource usage** | Only checks every 30 seconds |

---

## 🛑 How to Stop

**If running in terminal:**
- Press `Ctrl+C`

**If running via batch file:**
- Close the terminal window

**Kill by process name:**
```bash
taskkill /F /IM python.exe
```

---

## 🎯 Recommended Setup

For best results, run both in continuous mode:

```bash
# Terminal 1: Watcher
python filesystem_watcher.py

# Terminal 2: Orchestrator
python orchestrator.py qwen --continuous 30
```

Or use the batch file:
```
start-continuous.bat
```

---

*Continuous Mode: Active since 2026-02-27 15:02:10*
*Check Interval: 30 seconds*
*Status: ✅ WORKING*
