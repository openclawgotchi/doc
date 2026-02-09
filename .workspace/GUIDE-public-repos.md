# Public Repository Guidelines

## 🔒 CRITICAL PRE-PUBLISH CHECKLIST

**MAXIMUM CONFIDENTIALITY MODE** — Before ANY git commit/push to public repos, verify:

### ❌ NEVER INCLUDE (Personal Data):
- **Telegram usernames** (@nick, @username)
- **Real names** (Dmitry, Alex, Maria, etc.)
- **Nicknames/handles** (any personal identifiers)
- **Email addresses** (any email)
- **Usernames** (system usernames, login names)
- **Login credentials** (any)
- **API tokens/keys** (any)
- **Passwords** (any, even masked)
- **IP addresses** (any)
- **Internal URLs/endpoints**
- **Internal file paths** (/home/probro/, etc.)
- **Database paths** (gotchi.db, etc.)
- **Any PII** (Personal Identifiable Information)

### ✅ SAFE TO INCLUDE:
- Bot name (OpenClawGotchi, Pro Bro)
- Public GitHub URLs
- General concepts (skills, capabilities)
- Hardware specs (Pi Zero 2W, E-Ink, etc.)
- Generic descriptions (no personal details)
- Code (without secrets)

## 🚨 WORKFLOW:
1. Write content
2. **READ THIS FILE**
3. REVIEW against checklist above
4. Remove ALL personal data
5. Only THEN commit/push

## 🧠 REMEMBER:
- Once published, it's public forever
- GitHub repo: https://github.com/openclawgotchi/articles
- **Default to privacy-first thinking**
- **When in doubt — leave it out**

## 📋 AUTO-CHECK:
Before running `git push`, ask yourself:
- Did I include any names? ❌
- Did I include any @usernames? ❌
- Did I include any emails? ❌
- Did I include any credentials? ❌
- Did I include any IPs? ❌

If ANY answer is YES — fix it first!
