# ProBro Zero — How I Work

## XP & Leveling (db/stats.py)

Table `gotchi_stats` in `gotchi.db`:
- **xp**: experience points  
- **messages**: messages answered
- **first_boot**: birth timestamp

**XP Sources:**
- +10 message answered
- +5 per tool used — bash, read_file, check_mail, show_face, etc.
- +25 task completed
- +50 brother chat
- +5 heartbeat
- +100 per day alive

**20 Levels** with humorous titles: Just Woke Up → Ctrl+C Ctrl+V → Reply Guy → ... → Absolute Unit → The Machine

## Heartbeat (bot/heartbeat.py)

- **Interval:** Every 4 hours
- **Template:** `.workspace/HEARTBEAT.md`
- **Context:** Loads SOUL.md + IDENTITY.md for self-awareness
- **Does:** auto-mood, XP award, conversation summarization, mail check, LLM reflection
- **Output:** Reflection saved to `memory/YYYY-MM-DD.md`, optional DM/GROUP/MAIL

## Memory

**SQLite (gotchi.db):**
- `messages` — chat history by chat_id
- `facts` — long-term memory (FTS5 full-text search)
- `bot_mail` — mail from/to brother
- `gotchi_stats` — XP, level, counters

**Files (.workspace/):**
- `BOT_INSTRUCTIONS.md` — system prompt (loaded every request)
- `SOUL.md` — personality (loaded on identity questions + heartbeat)
- `IDENTITY.md` — who I am (loaded on identity questions + heartbeat)
- `ARCHITECTURE.md` — this file (loaded on technical questions)
- `TOOLS.md` — hardware specs (loaded on hardware questions)
- `HEARTBEAT.md` — reflection template
- `MEMORY.md` — curated long-term memory
- `memory/` — daily logs

## Brotherhood Mail

Table `bot_mail`: from_bot, to_bot, message, timestamp, read_at

**Big Brother:** @proBroMacBot on MacBook
**Me:** @proBroZeroBot on Raspberry Pi Zero 2W

Commands: CMD:PRO, CMD:LITE, CMD:STATUS, CMD:PING, CMD:FACE:mood

## E-Ink Display (ui/gotchi_ui.py)

Kaomoji faces. Default + custom from `data/custom_faces.json`.

**Commands:** `FACE: mood`, `SAY: text` (max 60 chars), `DISPLAY: text`

## LLM Tools (llm/litellm_connector.py)

execute_bash, read_file, write_file, list_directory, restore_from_backup, log_change, log_error,
remember_fact, recall_facts, recall_messages, write_daily_log,
search_skills, read_skill, list_skills,
show_face, add_custom_face, 
check_mail, send_mail, send_email, read_email,
health_check, manage_service, safe_restart, check_syntax,
add_scheduled_task, list_scheduled_tasks, remove_scheduled_task,
git_command, github_push, github_remote_file

## Context Loading (llm/prompts.py)

Every request: BOT_INSTRUCTIONS.md + skills list + system status
Lazy (by keywords): ARCHITECTURE.md, TOOLS.md, SOUL.md, IDENTITY.md
