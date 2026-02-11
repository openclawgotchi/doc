---
title: "Security Hardening"
date: 2026-02-10
type: "docs"
---

# Security Hardening — Protect Your Gotchi Bot

> Security is not optional for a 24/7 internet-connected AI bot

## 🔒 Overview

OpenClawGotchi runs 24/7 on Raspberry Pi Zero 2W with:
- Telegram Bot API access
- SSH daemon
- SQLite database with memories
- Potential external network exposure

**This guide hardens your installation against common attacks.**

## 🛡️ Essential Hardening

### 1. Change Default Passwords

\`\`\`bash
# Change pi user password
sudo passwd pi

# Or rename pi user entirely
sudo usermod -l gotchi pi
sudo usermod -d /home/gotchi -m gotchi
\`\`\`

### 2. Disable Password SSH Login

\`\`\`bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Set these values:
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no

# Restart SSH
sudo systemctl restart sshd
\`\`\`

### 3. Configure Firewall

\`\`\`bash
# Install ufw
sudo apt install ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (your IP only if possible)
sudo ufw allow from 192.168.31.0/24 to any port 22

# Allow outbound for bot (HTTP/HTTPS)
sudo ufw allow out 80/tcp
sudo ufw allow out 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
\`\`\`

### 4. Install Fail2ban

\`\`\`bash
sudo apt install fail2ban

# Configure for SSH
sudo nano /etc/fail2ban/jail.local
\`\`\`

\`\`ini
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
\`\`\`

\`\`\`bash
sudo systemctl restart fail2ban
\`\`\`

## 🔐 Token Security

### 1. Never Commit Tokens

Git repository should use \`<code>.gitignore</code>\`:

\`\`\`
# .gitignore
.env
*.db
__pycache__/
.DS_Store
\`\`\`

### 2. Rotate Tokens Regularly

- **Telegram Bot Token**: Revoke and regenerate via @BotFather every 3-6 months
- **API Keys**: Use environment variables, never hardcode

### 3. Least Privilege Principle

Bot should only have permissions it needs:
- Telegram: Bot API (no user API)
- LLM Provider: Model access only
- GitHub: Read-only for public repos

## 📊 Monitoring

### 1. Logwatch

\`\`\`bash
sudo apt install logwatch
# Configure daily email reports
sudo dpkg-reconfigure logwatch
\`\`\`

### 2. Auditd

\`\`\`bash
sudo apt install auditd
sudo systemctl enable auditd
sudo auditctl -w /home/gotchi/openclawgotchi -p wa -k gotchi
\`\`\`

### 3. Tripwire (File Integrity)

\`\`\`bash
sudo apt install tripwire
sudo tripwire --init
sudo tripwire --check
\`\`\`

## 🚨 Intrusion Detection

### Suspicious Activity Indicators

- Unknown login attempts in \`<code>/var/log/auth.log</code>\`
- Unexpected database changes
- New files in bot directory
- Increased CPU/memory usage
- Outbound network connections to unknown IPs

### Incident Response

If compromise suspected:

1. **Isolate**: Disconnect from network
2. **Preserve**: Don't reboot, save logs
3. **Analyze**: Check \`<code>auth.log</code>\`, database changes
4. **Recover**: Restore from backup, rotate all tokens
5. **Report**: Document incident, improve defenses

## 📦 Automated Hardening Script

The \`<code>harden.sh</code>\` script implements:

\`\`\`bash
# Watchdog timer
echo "Installing watchdog..."
sudo apt install watchdog
echo "watchdog-device = /dev/watchdog" | sudo tee -a /etc/watchdog.conf
sudo systemctl enable watchdog

# Log rotation
sudo apt install logrotate
\`\`\`

## 🧪 Testing Security

### Security Checklist

- [ ] SSH password login disabled
- [ ] Firewall enabled and configured
- [ ] Fail2ban running
- [ ] Tokens rotated in last 3 months
- [ ] No tokens in git repository
- [ ] Monitoring enabled
- [ ] Backup strategy in place
- [ ] Incident response plan documented

### Penetration Testing

\`\`\`bash
# Scan open ports
sudo nmap -sV localhost

# Check file permissions
find /home/gotchi/openclawgotchi -type f -perm -o+w

# Audit sudo access
sudo -l
\`\`\`

## 📝 Conclusion

Security is ongoing process, not one-time setup. Review this guide quarterly and after any security incident.

**Next:** [Skills Development](/doc/docs/skills-dev/) — Extend your bot's capabilities
