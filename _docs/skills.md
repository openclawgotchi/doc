# 🛠️ Skills Guide

Gotchi Bot has a powerful **skills system** — modular capabilities that can be loaded on demand. Skills are self-contained modules with their own documentation, requirements, and tools.

## How Skills Work

Each skill is defined in `gotchi-skills/` with a `skill.md` file containing:
- **Name & description** — what the skill does
- **Requirements** — required binaries, OS, environment variables
- **Documentation** — full usage guide
- **Tools** — optional tool definitions for LLM usage

The bot automatically loads available skills at startup and makes their tools accessible to the LLM.

---

## Available Skills

### 🛠️ Self-Improvement (Coding)

**Description:** Modify your own source code, understand project structure, add new features.

**Always active** — this is the core skill that enables self-modification.

**Capabilities:**
- Read and write any file in the project
- Understand project structure (modules, database, handlers, etc.)
- Add new Telegram commands
- Modify display behavior
- Update system prompts
- Add new LLM tools
- Edit database schema

**Key Tools:**
- `read_file(path)` — read any file
- `write_file(path, content)` — write file (creates backup)
- `check_syntax(file_path)` — validate Python syntax
- `git_command(command)` — run git operations
- `log_change(description)` — changelog entry
- `safe_restart()` — syntax check + restart

**Documentation:** [Full Coding Skill Guide](/coding/)

---

### 🖥️ Display Control

**Description:** Control E-Ink display - show faces, text, and status.

**Requirements:** Linux (Raspberry Pi)

**Capabilities:**
- Show 24+ built-in moods (happy, sad, excited, hacker, etc.)
- Display custom text with speech bubbles
- Full refresh to clear ghosting
- Add custom faces via JSON or code

**Key Commands:**
```
FACE: excited
SAY: Hello!
```

**Tools:**
- `add_custom_face(name, kaomoji)` — add persistent custom mood

**Documentation:** [Full Display Skill Guide](/display/)

---

### 🌤️ Weather

**Description:** Get current weather and forecasts using wttr.in — free, no API key needed!

**Requirements:** `curl` binary

**Capabilities:**
- Current weather for any city
- 3-day forecasts
- Compact format for E-Ink display
- No API key required

**Examples:**
```bash
# Quick format
curl -s "wttr.in/Moscow?format=3"
# Output: Moscow: ⛅️ +8°C

# Detailed
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# Output: London: ⛅️ +8°C 71% ↙5km/h
```

**Perfect for:** Heartbeat status updates, scheduled weather reports

---

### 🔧 System Administration

**Description:** Manage Raspberry Pi - power, services, monitoring, backups.

**Requirements:** Linux (Raspberry Pi)

**Capabilities:**
- Power management (reboot, shutdown)
- Service management (systemctl)
- System monitoring (temp, RAM, disk, CPU)
- Network diagnostics
- Process management
- Backup automation

**Key Commands:**
```bash
# Temperature
vcgencmd measure_temp

# Memory
free -h

# Service status
sudo systemctl status gotchi-bot

# Quick health check
echo "Temp: $(vcgencmd measure_temp), Uptime: $(uptime -p)"
```

**Perfect for:** Health checks, automated maintenance alerts

---

### 🎮 Discord Integration

**Description:** Send messages to Discord channels via webhook or bot.

**Requirements:** `curl` binary (webhook mode) or `discord.py` (bot mode)

**Capabilities:**
- Send simple text messages
- Rich embeds with colors and fields
- Custom username and avatar
- No bot token required (webhook mode)

**Setup (Webhook):**
1. Create webhook in Discord channel
2. Add to `.env`: `DISCORD_WEBHOOK=https://discord.com/api/webhooks/xxx/yyy`
3. Send: `curl -d '{"content":"Hello!"}' "$DISCORD_WEBHOOK"`

**Perfect for:** Heartbeat notifications, system alerts, daily summaries

---

## Reference Skills (OpenClaw Ecosystem)

The bot includes documentation for **50+ skills** from the OpenClaw ecosystem in `openclaw-skills/`. These are available for reference but may require:
- macOS (many are Mac-specific)
- Specific CLI tools not available on Pi
- Different hardware

Use `search_skills("query")` to find capabilities, then `read_skill("name")` to read documentation.

**Examples:**
- `github` — GitHub API integration
- `calendar` — Calendar events
- `email` — Email operations
- `music` — Music control
- `note` — Note-taking
- And 45+ more

---

## Adding New Skills

### Method 1: Simple Skill (No Code)

Just create a markdown file in `gotchi-skills/your-skill/skill.md`:

```markdown
---
name: Your Skill
description: What it does
metadata:
  {
    "openclaw": {
      "emoji": "🎯",
      "requires": { "bins": ["required-command"] },
      "always": false
    }
  }
---

# Your Skill

Documentation here...
```

The bot will automatically load it and the LLM can read the documentation!

### Method 2: Skill with Tools

Define tools in the skill's front matter. Tools become available to the LLM when the skill is loaded.

### Method 3: Python Module

For complex skills, create a Python module in `src/skills/` and wire it into the skill loader.

---

## Skill Philosophy

Gotchi skills follow these principles:

1. **Composable** — skills work independently
2. **Documented** — every skill has its own guide
3. **Gated** — requirements checked before loading
4. **Self-aware** — bot can read its own skill docs
5. **Extensible** — add new skills without touching core code

**The bot can teach you its own skills!** Just ask: "What can you do?" or "Tell me about the weather skill."

---

## Quick Reference

| Skill | Purpose | Active |
|-------|---------|--------|
| 🛠️ Coding | Self-modification | ✅ Always |
| 🖥️ Display | E-Ink faces | ✅ Always |
| 🌤️ Weather | Weather data | ✅ Yes |
| 🔧 System | Pi management | ✅ Yes |
| 🎮 Discord | Discord messages | ✅ Yes |

**All skills are documented and can be discovered by asking the bot!**
