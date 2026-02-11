---
title: "Skills Development"
date: 2026-02-10
type: "docs"
---

# Skills Development Guide

> Build custom capabilities for your Gotchi Bot

## 🎯 Overview

Gotchi Bot has a **modular skill system**:

- **Active Skills** — Loaded in \`<code>src/skills/</code>\`, can execute commands
- **Reference Skills** — Examples in \`<code>openclaw-skills/</code>\`, not loaded by default

## 📁 Skill Architecture

### Active Skills Structure

\`\`\`
src/skills/
├── __init__.py          # Skill registry
├── coding.py            # Code modification
├── display.py           # E-Ink control
├── weather.py           # Weather via wttr.in
├── system.py            # Pi administration
└── discord.py           # Discord messages
\`\`\`

### Skill Lifecycle

1. **Load** — Import on bot startup
2. **Register** — Add to \`<code>SKILL_HANDLERS</code>\` dict
3. **Match** — Check if user command triggers skill
4. **Execute** — Run skill handler
5. **Return** — Send response to user

## 🛠️ Creating a Custom Skill

### Step 1: Create Skill File

\`\`\`python
# src/skills/my_custom_skill.py

def handle(command: str, context: dict) -> str | None:
    """
    Handle custom commands
    Returns response string or None if not handled
    """
    if command.startswith("/hello"):
        return "Hello! I'm Gotchi Bot! 🤖"
    
    if command.startswith("/time"):
        from datetime import datetime
        return f"Current time: {datetime.now().strftime('%H:%M')}"
    
    return None  # Not handled
\`\`\`

### Step 2: Register Skill

\`\`\`python
# src/skills/__init__.py

from .my_custom_skill import handle

SKILL_HANDLERS = {
    "my_custom": handle,
    # ... other skills
}
\`\`\`

### Step 3: Test Your Skill

\`\`\`bash
# Restart bot
sudo systemctl restart gotchi-bot

# Test via Telegram
/hello
# Response: Hello! I'm Gotchi Bot! 🤖
\`\`\`

## 📚 Built-in Skills Reference

### coding — Code Modification

\`\`\`
/code refactor /home/gotchi/bot/main.py
/code add_feature "user authentication"
\`\`\`

**Capabilities:**
- Read and understand project structure
- Refactor existing code
- Add new features with tests
- Explain code changes

### display — E-Ink Control

\`\`\`
/face happy
/say "Hello World!"
/display clear
\`\`\`

**Capabilities:**
- Show pre-defined faces (happy, sad, thinking, etc.)
- Display text messages
- Clear screen
- Custom faces via \`<code>add_custom_face()</code>\`

### weather — Weather Info

\`\`\`
/weather
/weather London
\`\`\`

**Capabilities:**
- Current weather via wttr.in (no API key needed)
- Forecasts
- Multiple locations

### system — Pi Administration

\`\`\`
/system restart
/system status
/system update
\`\`\`

**Capabilities:**
- Restart bot service
- Show system stats (CPU, RAM, temp)
- Update packages
- View logs

## 🎨 Best Practices

### 1. Error Handling

\`\`\`python
def handle(command: str, context: dict) -> str | None:
    try:
        # Your skill logic
        result = do_something()
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
\`\`\`

### 2. Input Validation

\`\`\`python
def handle(command: str, context: dict) -> str | None:
    if not command.startswith("/myskill"):
        return None
    
    # Extract and validate argument
    parts = command.split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: /myskill <argument>"
    
    argument = parts[1].strip()
    if not argument:
        return "Argument cannot be empty"
\`\`\`

### 3. Use Caching

\`\`\`python
# Cache expensive API responses
import json
import time
from pathlib import Path

CACHE_FILE = Path("/tmp/weather_cache.json")

def get_cached_weather(location: str) -> dict | None:
    if not CACHE_FILE.exists():
        return None
    
    cache = json.loads(CACHE_FILE.read_text())
    if time.time() - cache["timestamp"] < 3600:  # 1 hour
        return cache.get(location)
    
    return None
\`\`\`

### 4. Logging

\`\`\`python
import logging

logger = logging.getLogger(__name__)

def handle(command: str, context: dict) -> str | None:
    logger.info(f"Processing command: {command}")
    # Your logic
\`\`\`

## 🔧 Advanced Skills

### Async Operations

\`\`\`python
import asyncio

async def async_handle(command: str, context: dict) -> str | None:
    # Async operations
    result = await fetch_api()
    return f"Result: {result}"
\`\`\`

### External APIs

\`\`\`python
import requests

def handle(command: str, context: dict) -> str | None:
    if command.startswith("/joke"):
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = response.json()
        return f"{joke['setup']} {joke['punchline']}"
\`\`\`

### Database Integration

\`\`\`python
import sqlite3

def handle(command: str, context: dict) -> str | None:
    if command.startswith("/note"):
        note = command.split(maxsplit=1)[1]
        
        conn = sqlite3.connect("data/notes.db")
        conn.execute("INSERT INTO notes (content) VALUES (?)", (note,))
        conn.commit()
        conn.close()
        
        return "Note saved!"
\`\`\`

## 🤝 Contributing Skills

Share your skills with the community!

1. **Fork** [openclawgotchi/openclawgotchi](https://github.com/openclawgotchi/openclawgotchi)
2. **Create** skill in \`<code>contrib/skills/</code>\`
3. **Test** thoroughly
4. **Submit** pull request

## 📖 Next Steps

- [XP & Memory System](/doc/docs/xp-memory/) — How the bot learns and remembers

**Happy coding!** 🚀
