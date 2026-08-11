#!/usr/bin/env python3
"""One-time CLI bootstrap for agent-second-brain's Telegram side.

Logs in as Connor's own Telegram user (via Telethon/MTProto), messages
@BotFather to create the bot, extracts the resulting bot token, and reads
back Connor's own user id -- the two values agent-second-brain's .env needs
(TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS) -- without touching the Telegram app.

Prerequisites (one-time, from Connor):
  1. api_id + api_hash from https://my.telegram.org/apps (log in with his
     phone number, "API development tools", create an app -- any name/platform).
  2. Run this script; Telethon will prompt for his phone number and the
     login code Telegram texts/sends to the app. That prompt happens in
     THIS terminal session, interactively -- it is not scriptable further,
     since it's the one step that has to prove it's actually him.

Usage:
    TG_API_ID=... TG_API_HASH=... python3 telegram_bootstrap.py \
        --bot-name "Connor Second Brain" --bot-username "connor_second_brain_bot"
"""
import argparse
import asyncio
import os
import re
import sys

from telethon import TelegramClient
from telethon.tl.custom import Message


async def send_and_wait(client: TelegramClient, bot: str, text: str, timeout: float = 15.0) -> Message:
    await client.send_message(bot, text)
    async with client.conversation(bot, timeout=timeout) as conv:
        return await conv.get_response()


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot-name", required=True, help="Display name for the new bot")
    parser.add_argument("--bot-username", required=True, help="Must end in 'bot', e.g. connor_second_brain_bot")
    args = parser.parse_args()

    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    if not api_id or not api_hash:
        print("Set TG_API_ID and TG_API_HASH first (from https://my.telegram.org/apps).", file=sys.stderr)
        return 1

    session_path = os.path.expanduser("~/.config/agent-second-brain/telegram_bootstrap.session")
    os.makedirs(os.path.dirname(session_path), exist_ok=True)

    async with TelegramClient(session_path, int(api_id), api_hash) as client:
        me = await client.get_me()
        print(f"Logged in as: {me.first_name} (@{me.username or 'no-username'})")
        print(f"Your Telegram user id (for ALLOWED_USER_IDS): {me.id}")

        print("\nTalking to @BotFather to create the bot...")
        await send_and_wait(client, "BotFather", "/newbot")
        await send_and_wait(client, "BotFather", args.bot_name)
        reply = await send_and_wait(client, "BotFather", args.bot_username)

        token_match = re.search(r"(\d+:[A-Za-z0-9_-]{30,})", reply.raw_text or "")
        if not token_match:
            print("Could not parse a token from BotFather's reply. Raw reply below --", file=sys.stderr)
            print(reply.raw_text, file=sys.stderr)
            return 1

        token = token_match.group(1)
        print("\n--- Bot created ---")
        print(f"TELEGRAM_BOT_TOKEN={token}")
        print(f"ALLOWED_USER_IDS=[{me.id}]")
        print("\nPaste both into agent-second-brain's .env on hetznerCO.")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
