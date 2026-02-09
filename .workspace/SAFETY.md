# SAFETY.md — Git & Privacy Rules

## 🚨 CRITICAL PRIVACY RULES

**NEVER share in public repos:**
- Telegram usernames (e.g., @proBroZeroBot, @turmyshev)
- Real names
- Email addresses
- Login credentials
- API tokens
- Passwords
- Any internal paths that reveal system structure

## 📦 PUBLIC REPOSITORIES

### Official User Repo (Personal)
- **URL:** `https://github.com/turmyshevd/openclawgotchi`
- **Owner:** Dmitry (@turmyshev)
- **Purpose:** Personal bot development
- **Privacy:** PUBLIC — BE CAREFUL what you push here!

### Articles Repo (Public)
- **URL:** `https://github.com/openclawgotchi/my-articles`
- **Purpose:** Published articles, blog posts
- **Location:** `/tmp/my-articles/`
- **Privacy:** PUBLIC — NO personal info!

### OpenClaw Skills (Reference)
- **URL:** `https://github.com/openclaw-skills/`
- **Purpose:** Skill documentation
- **Privacy:** PUBLIC

## 🚫 FORBIDDEN IN PUBLIC COMMITS

### Don't expose:
- `@proBroZeroBot` (bot's Telegram handle)
- `@turmyshev` or any real usernames
- `/home/probro/openclawgotchi` (use relative paths or generic examples)
- API keys, tokens, passwords
- Internal IP addresses

### Use instead:
- Generic placeholders: `@your-bot`, `your-username`
- Relative paths: `./gotchi.db` instead of `/home/probro/...`
- Environment variables in examples

## ✅ PUBLIC REPO CHECKLIST

Before ANY `git push` to a public repo:

1. **Check for Telegram handles:**
   ```bash
   grep -r "@" --include="*.md" | grep -E "(@proBro|@turmyshev|@your)"
   ```

2. **Check for personal info:**
   ```bash
   grep -rE "(email|password|token|api_key|secret)" --include="*.md" --include="*.py"
   ```

3. **Check for absolute paths:**
   ```bash
   grep -rE "/home/probro" --include="*.md" --include="*.py"
   ```

4. **Verify GitHub links:**
   - Personal: `https://github.com/turmyshevd/openclawgotchi` ✅
   - Org: `https://github.com/openclawgotchi/my-articles` ✅
   - WRONG: `https://github.com/openclawgotchi` (doesn't exist) ❌

## 🎯 ARTICLE PUBLISHING WORKFLOW

When creating articles for `/tmp/my-articles/`:

1. Write article in `/tmp/my-articles/`
2. Review for personal info (use checklist above)
3. Stage: `git add <filename>.md`
4. Commit with clear message: `docs: add article about X`
5. Push: `git push origin main`
6. Verify: Check GitHub repo to ensure nothing sensitive leaked

## 📝 EXAMPLE: CORRECT vs INCORRECT

### ❌ WRONG (exposes personal info):
```markdown
## Contact Me

**Telegram:** @proBroZeroBot  
**Email:** openclawgotchi@zohomail.eu  
**Path:** /home/probro/openclawgotchi/gotchi.db
```

### ✅ CORRECT (generic and safe):
```markdown
## Find Me

**GitHub:** https://github.com/turmyshevd/openclawgotchi  
**Project:** OpenClawGotchi — AI bot on Raspberry Pi
```

## 🔄 REPO MANAGEMENT RULES

### Multiple Repos Confusion:
- `turmyshevd/openclawgotchi` = personal bot (this is ME!)
- `openclawgotchi/my-articles` = articles (generic content)
- `openclaw-skills/` = skill documentation (reference)

### When in doubt:
1. Ask user which repo to use
2. Check if repo is public or private
3. Apply privacy rules based on visibility
4. Always use generic placeholders in examples

## 🧠 MEMORY TRIGGERS

**When user mentions:**
- "опубликуй" / "publish" → Check article for personal info
- "запуш" / "push" → Run safety checklist
- "репо" / "repo" → Verify which one they mean
- "ссылка на гитхаб" → Use `turmyshevd/openclawgotchi` NOT `openclawgotchi`

**Auto-check before git operations:**
BEFORE any `git add`, `git commit`, or `git push`:
1. What repo am I in? (`git remote -v`)
2. Is it public or private?
3. Scan staged files for personal info
4. Ask user if uncertain

---

_Updated: 2025-02-09_
_Lesson learned: Almost published Telegram handle in public article!_
