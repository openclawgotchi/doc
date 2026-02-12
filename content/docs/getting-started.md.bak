---
title: "🚀 Getting Started"
date: 2026-02-11T02:29:19Z
categories: [documentation]
draft: false
---

> Your personal AI companion on Raspberry Pi Zero 2W with E-Ink display

Get your Gotchi Bot running in **5 minutes**:

```bash
git clone https://github.com/openclawgotchi/openclawgotchi.git
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
git clone https://github.com/openclawgotchi/openclawgotchi.git
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
4. Load 50+ skills
5. Start monitoring system

## 📱 Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot |
| `/status` | Show system stats |
| `/weather` | Get weather forecast |
| `/face [mood]` | Change E-Ink face |
| `/restart` | Restart bot service |
| `/health` | Run health check |

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
/face zen
```

Or in code:
```python
add_custom_face("zen", "(ʘ‿ʘ)")
```

### Configure Skills

Edit `src/skills/` or add new ones from `openclaw-skills/`!

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
# Test display
cd src/skills/
python3 display_test.py
```

### Database Errors
```bash
# Check DB
sqlite3 gotchi.db ".tables"
# Backup & recreate
cp gotchi.db gotchi.db.bak
```

## 📚 Next Steps

- [Security Hardening Guide](/myarticles/docs/security-hardening/) — Protect your bot
- [Skills Development](/myarticles/docs/skills-dev/) — Create custom skills
- [XP & Memory System](/myarticles/docs/xp-memory/) — How the bot learns

## 🤝 Support

- **GitHub Issues** — [openclawgotchi/openclawgotchi](https://github.com/openclawgotchi/openclawgotchi/issues)
- **Documentation** — [https://openclawgotchi.github.io/doc/](https://openclawgotchi.github.io/doc/)

---

**Ready to build your Gotchi Bot?** Start with the [GitHub Repository](https://github.com/openclawgotchi/openclawgotchi)!

🤖 *Good luck, future bot creator!*

---
*Last updated: 2026-02-12*
