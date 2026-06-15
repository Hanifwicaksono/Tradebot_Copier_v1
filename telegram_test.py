from telethon import TelegramClient

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

client = TelegramClient("session_hanif", api_id, api_hash)

async def main():
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        try:
            print(dialog.name)
        except UnicodeEncodeError:
            clean_name = dialog.name.encode('ascii', errors='replace').decode('ascii')
            print(clean_name)

with client:
    client.loop.run_until_complete(main())