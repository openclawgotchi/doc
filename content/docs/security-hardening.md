# 🔐 Security Hardening & Optimization

## Overview

The `harden.sh` script optimizes your Raspberry Pi Zero 2W for running OpenClawGotchi 24/7. It's designed for **headless operation** — no monitor, no audio output needed on the Pi itself.

## What harden.sh Does

### 1. Swap Configuration (1GB)
**Critical for 512MB Pi Zero**

```bash
CONF_SWAPSIZE=1024  # 1GB swap file
```

**Why?** The bot + Python + Telegram API can exceed 512MB. Swap prevents crashes from Out-Of-Memory (OOM) killer.

---

### 2. Hardware Watchdog
**Auto-reboot on system freeze**

```bash
dtparam=watchdog=on          # BCM2835 watchdog in /boot/config.txt
RuntimeWatchdogSec=15        # Systemd timeout
```

**How it works:**
- If system freezes → watchdog resets the Pi after 15 seconds
- Protects against deadlocks, kernel panics, SD card corruption

---

### 3. Service Watchdog (Cron)
**Checks every 5 minutes**

```cron
*/5 * * * * systemctl is-active gotchi-bot.service >/dev/null || systemctl restart gotchi-bot.service
```

**Auto-healing:** If the bot crashes, it restarts automatically within 5 minutes.

---

### 4. Disable Unnecessary Services
**Saves 50-80MB RAM**

The following services are **disabled/masked**:

| Service | Purpose | RAM Saved |
|---------|---------|-----------|
| pipewire, pulseaudio | Audio output on Pi | ~40MB |
| bluetooth, hciuart | Bluetooth radio | ~10MB |
| avahi-daemon | Network discovery (mDNS) | ~5MB |
| cups | Printing | ~5MB |
| wayvnc | VNC server | ~10MB |
| ModemManager | Mobile broadband | ~5MB |

## ⚠️ Bluetooth Users: READ THIS!

**By default, harden.sh DISABLES Bluetooth** to save RAM.

### If you need Bluetooth:
- **BT speakers/headphones** for audio output
- **BT file transfer** from phone to Pi
- **BT keyboard/mouse** for debugging

### Solution 1: Skip harden.sh (if RAM is OK)
If you have plenty of free RAM (check with `free -h`), skip the hardening step:

```bash
./setup.sh      # Run setup only
# REBOOT, then test
```

### Solution 2: Re-enable Bluetooth after hardening
```bash
# Unmask and start Bluetooth
sudo systemctl unmask bluetooth hciuart
sudo systemctl start bluetooth hciuart
sudo systemctl enable bluetooth hciuart

# Verify
sudo systemctl status bluetooth
```

Then pair your devices:

```bash
# Enter Bluetoothctl
sudo bluetoothctl

# Scan for devices
scan on

# Pair (replace XX:XX:XX:XX:XX:XX with MAC)
pair XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX

# Exit
exit
```

### Solution 3: Modify harden.sh
Comment out the Bluetooth lines before running:

```bash
# In harden.sh, find:
# bluetooth hciuart

# Change to:
# bluetooth hciuart  # DISABLED — I need Bluetooth
```

---

## Post-Harden Verification

### Check RAM Usage
```bash
free -h
# Look for: Mem: available ~200MB+ free
```

### Check Watchdog
```bash
# Hardware watchdog in config.txt
grep watchdog /boot/config.txt

# Systemd watchdog
grep RuntimeWatchdogSec /etc/systemd/system.conf
```

### Check Service Watchdog (Cron)
```bash
sudo crontab -l | grep gotchi-bot
```

### Check Disabled Services
```bash
systemctl list-unit-files | grep masked
```

---

## Unhardening (if needed)

If you need to restore services:

```bash
# Restore Audio
sudo systemctl unmask pipewire pipewire-pulse wireplumber
systemctl --user unmask pipewire pipewire-pulse wireplumber
systemctl --user start pipewire pipewire-pulse wireplumber

# Restore Bluetooth
sudo systemctl unmask bluetooth hciuart
sudo systemctl start bluetooth hciuart

# Restore Avahi
sudo systemctl unmask avahi-daemon
sudo systemctl start avahi-daemon
```

---

## When to Run harden.sh

| Use Case | Run harden.sh? |
|----------|----------------|
| **Headless bot only** | ✅ Yes — recommended |
| Need Bluetooth audio | ⚠️ See "Bluetooth Users" above |
| Need local audio (3.5mm/HDMI) | ⚠️ Audio is disabled — restore pipewire |
| Debugging with monitor | ⚠️ Optional — but VNC is disabled |
| Development/testing | ❌ No — skip for flexibility |

---

## Summary

**Harden.sh = Stability + RAM optimization**

- ✅ Perfect for production 24/7 bot
- ✅ Auto-recovery from crashes
- ⚠️ Disables Bluetooth — restore if needed
- ⚠️ Disables audio — restore if using local sound

For most users: **Run it, restore Bluetooth if needed.** 

[Back to Getting Started](getting-started.md)
