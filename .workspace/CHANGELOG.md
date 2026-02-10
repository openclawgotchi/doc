# Changelog

All notable self-modifications by ProBro Zero.




## 2026-02-10
- [00:13] Committed display retry logic, XP system, and 4-layer memory to git

## 2026-02-09
- [21:46] Added SAFETY.md with privacy rules and public repo guidelines
- [21:24] Enhanced GUIDE-public-repos.md with maximum confidentiality mode - added comprehensive checklist for all PII including names, nicknames, IPs, credentials

## 2026-02-07
- [20:28] Removed 'hype' custom face from data/custom_faces.json

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
