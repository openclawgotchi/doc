---
title: "🛠️ Skills Development Guide"
date: 2026-02-11T02:29:19Z
categories: [documentation]
draft: false
---

ProBro Zero has a **two-tier skill system**:

1. **Active Skills** — Loaded and ready to use (in `src/skills/`)
2. **Reference Skills** — Passive knowledge base (in `openclaw-skills/`)

## Active Skills

Active skills are Python modules in `src/skills/` that can be executed.

### Current Active Skills

| Skill | Description | Commands |
|-------|-------------|----------|
| `coding` | Modify bot's own code, understand project structure | `/code`, `/refactor` |
| `display` | Control E-Ink display | `FACE:`, `SAY:`, `DISPLAY:` |
| `weather` | Get weather via wttr.in (no API key) | `/weather` |
| `system` | Pi administration: power, services, monitoring | `/system`, `/health` |
| `discord` | Send messages to Discord | `/discord` |

### Skill Structure

An active skill is a Python file with:

```python
## src/skills/your_skill.py

SKILL_INFO = {
    "name": "your_skill",
    "description": "What this skill does",
    "commands": ["command1", "command2"],
    "requires": []  # Dependencies: ["wifi", "api_key", etc.]
}

def main(action, *args):
    """
    Main entry point
    action: the command/verb to execute
    args: additional parameters
    """
    if action == "command1":
        return do_command1(args)
    # ...
```

### Registering a New Skill

1. **Create the file** in `src/skills/your_skill.py`
2. **Add to registry** in `src/skills/__init__.py`:

```python
from .your_skill import SKILL_INFO as YOUR_SKILL_INFO

ACTIVE_SKILLS = [
    # ... existing skills
    YOUR_SKILL_INFO,
]
```

3. **Restart the bot:** `/restart` or `safe_restart()`

## Reference Skills

Reference skills live in `openclaw-skills/` — they're documentation and examples from the OpenClaw ecosystem.

### Why Reference Skills?

- **50+ skills** available for reference
- Most require **macOS** or specific CLIs not available on Pi
- Use them as **learning material** or **adapt to Linux/Pi**

### Example Reference Skills

| Skill | Description | Platform |
|-------|-------------|----------|
| `alfred` | Alfred workflows | macOS |
| `keyboard` | Keyboard control | macOS |
| `notion` | Notion integration | Any (needs API) |
| `spotify` | Spotify control | macOS |

### Using Reference Skills

1. **Search:** `search_skills("query")` — find capabilities
2. **Read:** `read_skill("skill_name")` — get documentation
3. **Adapt:** If compatible, implement as active skill

## Skill Development Best Practices

### DO's

- Keep skills **modular** — one file per skill
- Return **structured responses** — dicts or formatted strings
- Handle **errors gracefully** — try/except with clear messages
- Document **requirements** in `SKILL_INFO`
- Use **built-in tools** first (see `TOOLS.md`)

### DON'Ts

- Don't hardcode secrets — use `.env`
- Don't block the event loop — use async or timeouts
- Don't duplicate existing tools — check `ARCHITECTURE.md` first
- Don't make heavy operations — Pi has limited RAM/CPU

## Examples

### Simple Skill: Timezones

```python
## src/skills/timezones.py

import zoneinfo
from datetime import datetime

SKILL_INFO = {
    "name": "timezones",
    "description": "Get time in different zones",
    "commands": ["time"],
    "requires": []
}

def main(action, *args):
    if action == "time":
        zone = args[0] if args else "UTC"
        try:
            tz = zoneinfo.ZoneInfo(zone)
            return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        except:
            return f"Unknown timezone: {zone}"
    return "Usage: /time <timezone>"
```

### Discord Skill Integration

```python
## src/skills/discord.py

import os
import requests

SKILL_INFO = {
    "name": "discord",
    "description": "Send messages to Discord",
    "commands": ["discord"],
    "requires": ["DISCORD_WEBHOOK_URL"]
}

def main(action, *args):
    if action == "send":
        webhook = os.getenv("DISCORD_WEBHOOK_URL")
        if not webhook:
            return "Error: DISCORD_WEBHOOK_URL not set"
        
        message = " ".join(args)
        payload = {"content": message}
        
        try:
            response = requests.post(webhook, json=payload)
            if response.status_code == 204:
                return "✅ Sent to Discord"
            else:
                return f"❌ Error: {response.status_code}"
        except Exception as e:
            return f"❌ Exception: {e}"
```

## Available Bot Tools

Skills have access to these built-in tools:

| Tool | Description |
|------|-------------|
| `execute_bash(command)` | Run shell commands |
| `read_file(path)` | Read file contents |
| `write_file(path, content)` | Write files |
| `check_syntax(file_path)` | Verify Python syntax |
| `show_face(mood)` | Change E-Ink display |
| `add_custom_face(name, kaomoji)` | Add new face |
| `remember_fact(category, fact)` | Save to facts DB |
| `recall_facts(query, limit)` | Search facts |
| `check_mail()` | Check brother bot mail |
| `health_check()` | Run system diagnostics |
| `schedule_task(...)` | Add scheduled task |
| `safe_restart()` | Restart after code changes |

## Skill Testing

### Manual Test

```bash
cd ~/openclawgotchi
python3 -m src.skills.your_skill
```

### Via Telegram

```
/your_skill command
```

### Debugging

```python
# In your skill
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Action: {action}, Args: {args}")
```

## Publishing Skills

### To Your Repo

```bash
git add src/skills/your_skill.py
git commit -m "feat: add your_skill"
git push
```

### To OpenClaw (if useful)

If your skill is generic and useful for others:
1. Fork https://github.com/openclawgotchi/openclaw-skills
2. Add your skill there
3. Submit PR

## See Also

- [Getting Started](/myarticles/docs/getting-started/) — First steps
- [Security Hardening](/myarticles/docs/security-hardening/) — Protect your bot
- [XP & Memory System](/myarticles/docs/xp-memory/) — How the bot learns

---
*Last updated: 2026-02-12*
