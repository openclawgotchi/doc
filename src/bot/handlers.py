"""
Telegram command and message handlers.
"""

import logging
import re

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from db.memory import (
    save_message, get_history, clear_history, get_message_count,
    save_user, add_fact, search_facts, get_recent_facts,
    save_pending_task, get_connection
)
from hardware.display import parse_and_execute_commands, error_screen, show_face
from hardware.system import get_stats
from llm.router import get_router
from llm.base import RateLimitError, LLMError
from bot.telegram import is_allowed, get_sender_name, send_long_message
from bot.onboarding import needs_onboarding, get_bootstrap_prompt, check_onboarding_complete, complete_onboarding
from hooks.runner import run_hook, HookEvent
from memory.flush import check_and_inject_flush, write_to_daily_log
from memory.summarize import optimize_history
from cron.scheduler import add_cron_job, list_cron_jobs, remove_cron_job
from skills.loader import get_eligible_skills
from config import LLM_PRESETS

log = logging.getLogger(__name__)


def _ensure_tool_usage_in_code_block(text: str) -> str:
    """Wrap Tool usage footer in ``` blocks if not already wrapped."""
    if "Tool usage" not in text:
        return text
    
    # Check if Tool usage is already inside a code block
    lines = text.split("\n")
    in_code_block = False
    tool_usage_line_idx = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        if "Tool usage" in line:
            tool_usage_line_idx = i
            break
    
    # If Tool usage found and NOT in code block, wrap it
    if tool_usage_line_idx is not None and not in_code_block:
        # Find where Tool usage section starts
        tool_start = tool_usage_line_idx
        # Insert ``` before Tool usage
        lines.insert(tool_start, "```")
        # Find end of Tool usage section (next empty line or end)
        tool_end = tool_start + 1
        while tool_end < len(lines) and lines[tool_end].strip() and not lines[tool_end].strip().startswith("FACE:"):
            tool_end += 1
        # Insert ``` after Tool usage section
        lines.insert(tool_end, "```")
    
    return "\n".join(lines)


# --- Command Handlers ---

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        if chat.type == "private":
            await update.message.reply_text("Access denied.")
        return
    
    save_user(user.id, user.username or "", user.first_name or "", user.last_name or "")
    
    # Fire command hook
    run_hook(HookEvent(
        event_type="command",
        action="/start",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm your AI assistant on Raspberry Pi.\n\n"
        f"*Commands:*\n"
        f"/status — system & XP\n"
        f"/xp — XP rules & progress\n"
        f"/context — view/trim context window\n"
        f"/clear — wipe conversation history\n"
        f"/pro — switch to Pro mode\n"
        f"/lite — switch to Lite mode\n"
        f"/mode — toggle Lite/Pro mode\n"
        f"/memory — database stats\n\n"
        f"*Memory:*\n"
        f"/remember <cat> <fact> — save fact\n"
        f"/recall <query> — search memory\n\n"
        f"*Automation:*\n"
        f"/cron <name> <min> <msg> — schedule task\n"
        f"/jobs — list/remove tasks"
    , parse_mode="Markdown")


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    # Fire command hook
    run_hook(HookEvent(
        event_type="command",
        action="/clear",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    clear_history(chat.id)
    await update.message.reply_text("History cleared.")


async def cmd_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /context command — show context window status."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    from config import HISTORY_LIMIT, MODEL_CONTEXT_TOKENS
    
    msg_count = get_message_count(chat.id)
    history = get_history(chat.id)  # last HISTORY_LIMIT messages only
    
    # Tokens actually sent to model (history only; system prompt is extra)
    total_chars = sum(len(m.get("content", "")) for m in history)
    est_tokens = total_chars // 4
    # Model context window usage (history vs model limit)
    usage_pct_model = min(100, (est_tokens * 100) // MODEL_CONTEXT_TOKENS)
    filled = min(10, (usage_pct_model * 10) // 100)
    bar = "█" * filled + "░" * (10 - filled)
    
    msg = (
        f"📊 *Context Window*\n\n"
        f"*Model window:* ~{est_tokens:,} / {MODEL_CONTEXT_TOKENS:,} tokens\n"
        f"{bar} {usage_pct_model}%\n\n"
        f"*Messages in DB:* {msg_count}\n"
        f"*In context:* {len(history)} / {HISTORY_LIMIT}\n\n"
    )
    
    if usage_pct_model > 80:
        msg += "_⚠️ Context nearly full. Trim soon._"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pro command — switch to Pro mode."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    run_hook(HookEvent(
        event_type="command",
        action="/pro",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    # Switch to Pro mode (store in user preferences or session)
    # For now, just confirm
    await update.message.reply_text("🧠 Pro mode activated. Using full model.")


async def cmd_lite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lite command — switch to Lite mode."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    run_hook(HookEvent(
        event_type="command",
        action="/lite",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    await update.message.reply_text("⚡ Lite mode activated. Using faster model.")


async def cmd_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mode command — toggle Lite/Pro mode."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    run_hook(HookEvent(
        event_type="command",
        action="/mode",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    await update.message.reply_text("🔄 Mode toggled.")


async def cmd_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /memory command — database stats."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    run_hook(HookEvent(
        event_type="command",
        action="/memory",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    from db.stats import get_memory_stats
    stats = get_memory_stats()
    
    msg = (
        f"💾 *Memory Stats*\n\n"
        f"*Messages:* {stats.get('messages', 0)}\n"
        f"*Facts:* {stats.get('facts', 0)}\n"
        f"*Tasks:* {stats.get('tasks', 0)}\n"
        f"*Users:* {stats.get('users', 0)}\n"
    )
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_remember(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /remember command — save a fact."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /remember <category> <fact>")
        return
    
    category = context.args[0]
    fact = " ".join(context.args[1:])
    
    add_fact(category, fact, user.id)
    
    run_hook(HookEvent(
        event_type="command",
        action="/remember",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    await update.message.reply_text(f"✅ Remembered: [{category}] {fact}")


async def cmd_recall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /recall command — search memory."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /recall <query>")
        return
    
    query = " ".join(context.args)
    facts = search_facts(query, limit=10)
    
    if not facts:
        await update.message.reply_text(f"No facts found for: {query}")
        return
    
    msg = f"🔍 *Recall: {query}*\n\n"
    for f in facts:
        msg += f"*[{f['category']}]* {f['fact']}\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_cron(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cron command — schedule a task."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /cron <name> <minutes> <message>")
        return
    
    name = context.args[0]
    try:
        minutes = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Minutes must be a number.")
        return
    
    message = " ".join(context.args[2:])
    
    add_cron_job(name, minutes, message, chat.id)
    
    run_hook(HookEvent(
        event_type="command",
        action="/cron",
        user_id=user.id,
        chat_id=chat.id,
        username=get_sender_name(user)
    ))
    
    await update.message.reply_text(f"⏰ Scheduled: {name} in {minutes} min")


async def cmd_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /jobs command — list/remove tasks."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    jobs = list_cron_jobs()
    
    if not jobs:
        await update.message.reply_text("No scheduled tasks.")
        return
    
    msg = "⏰ *Scheduled Tasks*\n\n"
    for job in jobs:
        msg += f"• {job['name']} — {job['minutes']} min\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_xp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /xp command — show XP rules and progress."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    from db.stats import get_xp, get_level_info
    
    xp = get_xp()
    level_info = get_level_info()
    
    msg = (
        f"⭐ *XP & Level*\n\n"
        f"*Current XP:* {xp:,}\n"
        f"*Level:* {level_info['level']} — {level_info['rank']}\n"
        f"*Next level:* {level_info['next_xp']:,} XP\n"
        f"*Progress:* {level_info['progress']}%\n\n"
        f"*How to earn XP:*\n"
        f"+10 per message\n"
        f"+5 per tool use\n"
        f"+25 per task completion\n"
        f"+100 per day alive"
    )
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command — system & XP."""
    user = update.effective_user
    chat = update.effective_chat
    
    if not is_allowed(user.id, chat.id):
        return
    
    from db.stats import get_xp, get_level_info
    
    stats = get_stats()
    xp = get_xp()
    level_info = get_level_info()
    
    msg = (
        f"🎮 *Level:* {level_info['level']} ({level_info['rank']})\n"
        f"⭐ *XP:* {xp:,}\n"
        f"💬 *Messages:* {stats.get('message_count', 0)}\n"
        f"⏱️ *Uptime:* {stats.get('uptime', 'Unknown')}\n"
        f"🌡️ *Temperature:* {stats.get('temp', 'Unknown')}\n"
        f"💾 *RAM Free:* {stats.get('ram_free', 'Unknown')}\n"
    )
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command — alias for /status."""
    await cmd_status(update, context)


# --- Message Handlers ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages — main conversation flow."""
    user = update.effective_user
    chat = update.effective_chat
    conv_id = chat.id
    
    if not is_allowed(user.id, conv_id):
        return
    
    user_text = update.message.text
    sender = get_sender_name(user)
    
    log.info(f"[{conv_id}] {sender}: {user_text[:50]}")
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=conv_id, action=ChatAction.TYPING)
    
    # Save user message
    save_message(conv_id, "user", user_text)
    
    try:
        # === LLM CALL ===
        connector = get_router().get_connector()
        response = await connector.get_response(conv_id, user_text)
        
        # === PARSE SPECIAL COMMANDS ===
        # Extract MAIL:, REMEMBER:, etc.
        cmds = parse_and_execute_commands(response, update, context, user)
        
        # Build clean text for Telegram (remove commands)
        clean_text = response
        
        # Remove MAIL: blocks (they were processed)
        if cmds.get("mail"):
            lines = clean_text.split("\n")
            clean_text = "\n".join(
                l for l in lines
                if not l.strip().upper().startswith("MAIL:")
            )
        
        # Remove REMEMBER: blocks (they were processed)
        if cmds.get("remember"):
            lines = clean_text.split("\n")
            clean_text = "\n".join(
                l for l in lines
                if not l.strip().upper().startswith("REMEMBER:")
            )
        
        # === FIX: Ensure Tool usage is in code block ===
        clean_text = _ensure_tool_usage_in_code_block(clean_text)
        
        # Mode indicator only for Pro (Lite = default, no label)
        if connector != "litellm":
            clean_text += "\n\n🧠 Pro"
        
        await send_long_message(update, clean_text, parse_mode="Markdown" if connector == "litellm" else None)

        # AWARD XP LAST — Avoid Level Up overwriting the response on E-Ink
        from db.stats import on_message_answered, on_tool_use
        on_message_answered()
        
        # Count tool actions from response footer for XP bonus
        tool_match = re.search(r'Tool usage \((\d+)\):', response)
        if tool_match:
            on_tool_use(int(tool_match.group(1)))
        # Also count parsed commands (MAIL:, REMEMBER:) as tool-like actions
        elif cmds.get("mail") or cmds.get("remember"):
            on_tool_use(sum(1 for k in ("mail", "remember") if cmds.get(k)))
            
    except RateLimitError:
        # Queue for later
        save_pending_task(conv_id, user_text, sender, is_group)
        await update.message.reply_text("💤 Rate limited. Queued for later.")
        
        # Show on screen
        error_screen("Rate Limit")
        
        from audit_logging.command_logger import log_error
        log_error("rate_limit", "Claude rate limited", {"chat_id": conv_id})
        
    except LLMError as e:
        log.error(f"LLM error: {e}")
        await update.message.reply_text(f"Error: {e}")
        
        # Show on screen
        error_screen(str(e))
        
        from audit_logging.command_logger import log_error
        log_error("llm_error", str(e), {"chat_id": conv_id})
        
    except Exception as e:
        log.exception(f"Handler error: {e}")
        await update.message.reply_text(f"Something broke: {e}")
        
        error_screen("Error")
        
        from audit_logging.command_logger import log_error
        log_error("handler_error", str(e), {"chat_id": conv_id})
    
    finally:
        # Check for flush/summary triggers (context optimization)
        check_and_inject_flush(conv_id)
        optimize_history(conv_id)
