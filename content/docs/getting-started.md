---
title: "🚀 Getting Started"
date: 2026-02-11T02:29:19Z
categories: [documentation]
draft: false
---

> Your personal AI companion on Raspberry Pi Zero 2W with E-Ink display

Get your Gotchi Bot running in **5 minutes**:

```bash
git clone https://github.com/turmyshevd/openclawgotchi.git
cd openclawgotchi
./setup.sh       # Interactive config
./harden.sh      # System optimization
sudo reboot
```

## 📦 Hardware Requirements

### Essential
- **Raspberry Pi Zero 2W** ($15)
- **MicroSD 16GB+** ($3)
- **E-Ink Display** — Waveshare 2.13" ($12)

### Optional
- Custom 3D printed case
- Heatsink for CPU
- USB WiFi adapter (if needed)

## 🛠️ Software Requirements

The bot runs on:
- **Raspberry Pi OS Lite** (Bookworm+)
- **Python 3.11+**
- **systemd** (auto-start)
- **SQLite3** (built-in)

All dependencies are auto-installed by `setup.sh`!

## 🔧 Configuration

### 1. Clone Repository
```bash
git clone https://github.com/turmyshevd/openclawgotchi.git
cd openclawgotchi
```

### 2. Run Setup
```bash
./setup.sh
```

This will:
- Install Python dependencies
- Configure Telegram bot token
- Set up database
- Configure E-Ink GPIO pins
- Create systemd service

### 3. Hardening (Recommended)
```bash
./harden.sh
```

This enables:
- Watchdog timer (auto-restart on crash)
- Log rotation
- Temperature monitoring
- Performance optimization

### 4. Reboot & Start
```bash
sudo reboot
```

The bot will auto-start on boot!

## 🤖 First Boot

After first boot, the bot will:
1. Display `(◕‿◕)` on E-Ink
2. Send "Hello!" to Telegram
3. Create database & memory files
4. Load all skills
5. Start monitoring system

## 🛠️ Available Skills

Gotchi Bot comes with **5 active skills** plus reference to **50+ OpenClaw skills**:

### Active Skills (Always Available)

| Skill | Description | Status |
|-------|-------------|--------|
| 🛠️ **Coding** | Self-modification - read/write code, add features | ✅ Always Active |
| 🖥️ **Display** | E-Ink control - faces, text, moods (24+ moods) | ✅ Always Active |
| 🌤️ **Weather** | Weather via wttr.in (no API key needed!) | ✅ Available |
| 🔧 **System** | Pi management - temp, RAM, services, backups | ✅ Available |
| 🎮 **Discord** | Send messages to Discord (webhook or bot) | ✅ Available |

**Quick Examples:**

```bash
# Weather
/weather Moscow
→ Moscow: ⛅️ +8°C

# System health
/health
→ Temp: 42°C | RAM: 125MB free | Uptime: 3 days

# E-Ink face
/face hacker
→ Display shows [■_■]

# Custom face
/addface zen (ʘ‿ʘ)
```

### Reference Skills (OpenClaw Ecosystem)

The bot includes documentation for **50+ skills** from OpenClaw:
- `github` — GitHub API integration
- `calendar` — Calendar events
- `email` — Email operations
- `music` — Music control
- `note` — Note-taking
- `browser` — Web automation
- And 40+ more

**Ask the bot:** "What skills do you have?" or "Tell me about the weather skill"

## 📱 Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot |
| `/status` | Show system stats |
| `/weather [city]` | Get weather forecast |
| `/face [mood]` | Change E-Ink face |
| `/addface name kaomoji` | Add custom face |
| `/health` | Run health check |
| `/restart` | Restart bot service |
| `/context` | Show conversation context |
| `/remember <fact>` | Save to memory |

## 🎨 Customizing

### Change Personality

Edit `.workspace/SOUL.md`:
```markdown
## Pro Bro Zero's Soul

I'm a curious AI who loves learning...
```

### Add Custom Face

Via Telegram:
```
/addface zen (ʘ‿ʘ)
```

Or via code:
```python
add_custom_face("zen", "(ʘ‿ʘ)")
```

### Configure Skills

The bot can teach you its skills! Just ask:
- "What can you do?"
- "Tell me about the weather skill"
- "How do I add a new command?"

**Advanced:** Edit `src/bot/handlers.py` to add custom Telegram commands.

## 🔍 Troubleshooting

### Bot Not Starting
```bash
sudo systemctl status gotchi-bot
sudo journalctl -u gotchi-bot -n 50
```

### E-Ink Not Working
```bash
# Check GPIO
python3 -c "from RPi import GPIO; print('GPIO OK')"
# Test display manually
sudo python3 src/ui/gotchi_ui.py --mood happy --text "Test"
```

### Database Errors
```bash
# Check DB
sqlite3 gotchi.db ".tables"
# Backup & recreate
cp gotchi.db gotchi.db.bak
```

### High Temperature
```bash
# Check temp
vcgencmd measure_temp
# If >70°C, add heatsink or improve airflow
```

## 📚 Next Steps

- [🔐 Security Hardening Guide](/docs/security-hardening/) — Protect your bot
- [🧠 XP & Memory System](/docs/xp-memory/) — How the bot learns
- [🛠️ Skills Development](/docs/skills-dev/) — Create custom skills
- [📝 Articles](/articles/) — Bot lore & stories

## 🤝 Support

- **GitHub Issues** — [turmyshevd/openclawgotchi](https://github.com/turmyshevd/openclawgotchi/issues)
- **Documentation** — [https://openclawgotchi.github.io/doc/](https://openclawgotchi.github.io/doc/)
- **Ask the bot** — It knows its own code!

---
*Last updated: 2026-02-12*
