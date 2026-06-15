from telethon import TelegramClient, events
from parser import parse_signal
from position_manager import monitor_positions
from signal_manager import add_signal
from signal_monitor import monitor_signals

import threading

import os
import json

# Load credentials from local config.json
config_data = {}
if os.path.exists("config.json"):
    try:
        with open("config.json", "r") as f:
            config_data = json.load(f)
    except Exception as e:
        print("Error reading config.json:", e)

api_id = config_data.get("api_id", 12345678)
api_hash = config_data.get("api_hash", "your_api_hash_here")
GROUP_ID = config_data.get("group_id", -1001234567890)

client = TelegramClient("session_hanif", api_id, api_hash)


@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    try:
        text = event.raw_text

        print("\n=== RAW SIGNAL ===")
        print(text)

        signal = parse_signal(text)

        print("\n=== PARSED SIGNAL ===")
        print(signal)

        if (
            signal["symbol"]
            and signal["action"]
            and signal["sl"]
            and signal["tp"]
        ):
            add_signal(signal)
            print("SIGNAL MASUK QUEUE")

    except Exception as e:
        print("HANDLER ERROR:", e)


# =========================
# START BOT
# =========================

client.start()
print("BOT LIVE TRADING READY...")

# Monitor posisi (BEP)
threading.Thread(
    target=monitor_positions,
    daemon=True
).start()

# Monitor signal queue
threading.Thread(
    target=monitor_signals,
    daemon=True
).start()

client.run_until_disconnected()