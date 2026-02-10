# MEMORY — Static Long-Term Context

This file contains manually curated facts about the owner, system, and project. 
It serves as **static context** that complements the dynamic SQLite `facts` table.

**Two memory systems work together:**
1. **SQLite `facts` table** (dynamic, searchable via `/remember` and `/recall`)
2. **This file** (static, human-editable reference)

---

## Owner
- See USER.md for details
- Russian-speaking, technical
- Works with Pi, Arduino, RP2040, web dev

## System
- Raspberry Pi Zero 2W, 512MB RAM, 1GB swap
- Bot runs as systemd service with cron watchdog
- Memory architecture: SQLite with `messages` (short-term) + `facts` (long-term FTS5)

## Preferences
- (to be filled after first conversation)

## Ecosystem
- Shared group for bot-to-bot messaging (see .env for group ID)
- Both bots need Privacy Mode disabled in BotFather for bot-to-bot messaging

## Notable Events
- 2026-02-01: Template system v1 deployed
- 2026-02-01: Bot-to-bot group configured
- 2026-02-03: Refactored memory system (unified SQLite with FTS5)
