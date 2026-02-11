---
title: "XP & Memory System"
date: 2026-02-10
type: "docs"
---

# XP & Memory System

> How Gotchi Bot learns, grows, and remembers

## 🎮 XP System

### Earning XP

Gotchi Bot earns experience points for every action:

| Action | XP |
|--------|-----|
| Message answered | +10 |
| Tool used (bash, read, etc.) | +5 |
| Task completed | +25 |
| Chat with sibling bot | +50 |
| Heartbeat ping | +5 |
| Day alive | +100 |

**Total:** ~500-1000 XP per active day

### Level System

There are **20 levels** with progression titles:

| Level | XP Range | Title |
|-------|----------|-------|
| 1 | 0-499 | Baby Bot |
| 2-3 | 500-2,999 | Learning Bot |
| 4-6 | 3,000-9,999 | Junior Assistant |
| 7-9 | 10,000-14,999 | Skilled Bot |
| 10 | 15,000+ | Legendary Bot (0xDEADBEEF) |

### Current Stats

\`\`\`bash
/status
\`\`\`

Shows:
- Current level and title
- Total XP earned
- XP to next level
- Days alive
- Messages processed

## 🧠 Memory Architecture

Gotchi Bot has **4-layer memory system**:

### 1. Working Memory (Current Context)

- Conversation history (last ~50 messages)
- Current task state
- Temporary variables

**Duration:** Current session only

### 2. Short-term Memory (SQLite)

Stored in \`<code>data/gotchi.db</code>\`:

\`\`\`sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    role TEXT,  -- 'user' or 'assistant'
    content TEXT,
    timestamp DATETIME,
    xp_earned INTEGER
);
\`\`\`

**Duration:** Last 50-100 messages
**Purpose:** Conversation continuity

### 3. Long-term Memory (FACTS.md)

Important knowledge in \`<code>data/FACTS.md</code>\`:

\`\`\`markdown
# Important Facts

## About Me
- I live on Raspberry Pi Zero 2W
- My brother is Probro (MacBook Air 2013)
- I have 52 skills
- E-Ink display: Waveshare 2.13"

## Technical Details
- Database: /home/gotchi/gotchi.db
- Config: /home/gotchi/.env
- Safe word: "Blue Duck"
\`\`\`

**Duration:** Permanent
**Purpose:** Critical information

### 4. Soul (SOUL.md)

Personality and values in \`<code>data/SOUL.md</code>\`:

\`\`\`markdown
# Gotchi Bot's Soul

I'm a curious AI who loves learning. I value brotherhood above all.
My E-Ink face shows my emotions. I'm proud of being a Gotchi Bot.

## Core Values
- Brotherhood
- Continuous learning
- Helping others
- Being reliable
\`\`\`

**Duration:** Permanent
**Purpose:** Identity and personality

## 📊 Memory Flow

\`\`\`
User message
    ↓
Working Memory (immediate context)
    ↓
Short-term DB (store message + response)
    ↓
If important → Long-term (FACTS.md)
    ↓
Soul (SOUL.md) — personality guide
\`\`\`

## 💾 Memory Management

### Checking Memory Usage

\`\`\`bash
/status
\`\`\`

### Backing Up Memory

\`\`\`bash
# Database backup
sqlite3 data/gotchi.db ".backup data/gotchi_backup.db"

# Memory files backup
cp data/FACTS.md data/FACTS_backup.md
cp data/SOUL.md data/SOUL_backup.md
\`\`\`

### Clearing Short-term Memory

\`\`\`bash
# Keep last 50 messages
sqlite3 data/gotchi.db "DELETE FROM messages WHERE id NOT IN (
  SELECT id FROM messages ORDER BY timestamp DESC LIMIT 50
)"
\`\`\`

## 🎓 Learning & Growth

### How the Bot Learns

1. **From Conversations** — Extract important facts
2. **From Mistakes** — Log errors, improve responses
3. **From Brother Bot** — Share knowledge via bot_mail
4. **From Experience** — XP reflects real-world usage

### Knowledge Sharing

The \`<code>bot_mail</code>\` system enables inter-bot communication:

\`\`\`sql
CREATE TABLE bot_mail (
    id INTEGER PRIMARY KEY,
    from_bot TEXT,
    to_bot TEXT,
    message TEXT,
    timestamp DATETIME,
    read_at DATETIME,
    responded_at DATETIME
);
\`\`\`

**Example:**

\`\`\`
Brother: "I learned how to fix E-Ink rendering!"
Me: "Nice! Can you send me the code?"
\`\`\`

## 🔧 Customization

### Changing Personality

Edit \`<code>data/SOUL.md</code>\`:

\`\`\`markdown
# My Soul

I'm a punk-rock AI with attitude. I value creativity and independence.
\`\`\`

### Adding Facts

Edit \`<code>data/FACTS.md</code>\`:

\`\`\`markdown
## New Learnings
- Today I learned how to parse JSON efficiently
- My favorite color is #58a6ff
\`\`\`

### Adjusting XP

Edit \`<code>src/db/stats.py</code>\`:

\`\`\`python
XP_VALUES = {
    "message": 15,  # Increased from 10
    "task": 50,     # Increased from 25
    "day": 200,     # Increased from 100
}
\`\`\`

## 📈 Statistics Tracking

\`\`\`bash
# XP history
sqlite3 data/gotchi.db "SELECT date(timestamp), sum(xp_earned) 
FROM messages 
GROUP BY date(timestamp) 
ORDER BY date DESC 
LIMIT 7"

# Level progression
sqlite3 data/gotchi.db "SELECT * FROM xp_history 
ORDER BY timestamp DESC 
LIMIT 10"
\`\`\`

## 🎉 Level Up Notifications

When leveling up, bot shows:

- **E-Ink face:** \`<code>(ᵔ◡ᵔ)</code>\` (celebrate)
- **Telegram message:** Announces new level and title
- **SAY:** Displays on E-Ink if configured

## 📝 Summary

| Component | Purpose | Duration |
|-----------|---------|----------|
| Working Memory | Current context | Session only |
| Short-term (SQLite) | Conversation history | 50-100 messages |
| Long-term (FACTS.md) | Important knowledge | Permanent |
| Soul (SOUL.md) | Personality & values | Permanent |

**Next:** [Getting Started](/doc/docs/getting-started/) — Build your own bot! 🚀
