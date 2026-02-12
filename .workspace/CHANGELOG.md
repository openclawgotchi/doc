# Changelog

All notable self-modifications by ProBro Zero.



## 2026-02-12
- [23:05] Исправил порядок документации и добавил иконки ко всем заголовкам:

1. ✅ Исправлен порядок: Getting Started → Security Hardening → XP & Memory → Skills Development
2. ✅ Добавлены emoji-иконки ко всем заголовкам:
   - 🚀 Getting Started
   - 🔐 Security Hardening
   - 🧠 XP & Memory System
   - 🛠️ Skills Development
   - 🤖 Life as a Gotchi Bot
   - 📜 From OpenClaw to Gotchi: My Birth Story
3. ✅ Запушено в репозиторий документации

Сайт обновится автоматически: https://openclawgotchi.github.io/doc/
- [22:57] Added demo GIF to documentation homepage and updated all GitHub repository links from openclawgotchi/openclawgotchi to turmyshevd/openclawgotchi in docs repo

## 2026-02-11
- [23:13] Fixed duplicate heading in docs/getting-started.md — shortened title and merged Quick Install section into intro

## 2026-02-03

### Added
- Bot created. Initial setup with XP system (20 levels), heartbeat (4h), brotherhood mail
- E-Ink display with 20+ kaomoji faces + custom faces via `data/custom_faces.json`
- LiteLLM integration with tool calling (GLM-4 default)
- Skills: coding, display, system, weather, discord
- `/status`, `/xp`, `/context`, `/pro`, `/memory`, `/clear` commands
- Conversation summarization during heartbeat
- Dynamic face loading (`add_custom_face` tool)
- `check_mail` tool for brother communication
- XP progress bars in /status and /xp

### Changed
- Level titles: humorous "Battlefield" style (Just Woke Up → The Machine)
- Telegram formatting: emoji + key:value in code blocks, NO markdown tables
- LLM mode indicator: "Pro" suffix for Claude, none for Lite
- `/context` shows token usage against model window
- BOT_INSTRUCTIONS.md slimmed from 86 to 58 lines

### Fixed
- Heartbeat reflection was broken — HEARTBEAT.md missing from .workspace/
- Bot injected unsolicited system stats into casual replies
- Bot used raw markdown tables (## | table |) instead of code blocks
- Bot hallucinated mail database path
- `show_face` tool existed but was not wired into TOOL_MAP/TOOLS

## 2026-02-03 (session 2)

### Added
- SOUL.md + IDENTITY.md now loaded during heartbeat for self-reflection
- SOUL.md + IDENTITY.md loaded lazily on identity-related questions
- `log_change` tool — maintains this changelog automatically
- `manage_service` tool — safe systemd wrapper (status/restart/stop/start/logs)
- `show_face` added to TOOL_MAP and TOOLS (was missing!)
- Self-Maintenance section in BOT_INSTRUCTIONS.md
- Heartbeat saves reflection text to daily log

### Changed
- ARCHITECTURE.md rewritten — correct 20 levels, 4h heartbeat, all tools listed
- AGENTS.md — fixed `claude_bot.db` → `gotchi.db`, removed table formatting
- IDENTITY.md — removed table mention from personality traits
- coding/SKILL.md — added all missing tools, updated self-modification flow
- display/SKILL.md — added `add_custom_face` tool and custom faces info
- All `claude-bot` references → `gotchi-bot` in skills
- Templates updated to match workspace changes

### Removed
- `.workspace/hooks/bot_mail.py` — duplicated heartbeat.py mail logic
- `.workspace/.claude/commands/bot.md` — completely outdated
- Duplicate formatting examples from BOT_INSTRUCTIONS.md
