# MT5 Telegram Auto-Trader Bot

This is a MetaTrader 5 (MT5) Auto-Trading Bot that listens for trading signals from a Telegram channel/group, parses them, monitors the entry zone, executes trades on MT5, and manages active positions with a Break-Even (BE) protection feature.

---

## Features

- **Telegram Listener**: Listens to messages from a specific Telegram channel or group using Telethon.
- **Signal Parser**: Automatically parses signal actions (`BUY` or `SELL`), entry price ranges, Stop Loss (`SL`), and Take Profit (`TP`) levels using regular expressions. Defaults to trading **XAUUSD** (Gold).
- **Signal Queue & Expiration**: Saves signals to `active_signals.json` to prevent duplicates. Signals expire if the first take-profit target is reached before the price enters the entry zone.
- **Auto-Execution**: Places market trades on MT5 with customizable lot sizes (default: `0.01`). Includes filling mode fallbacks (`FOK`, `RETURN`, `IOC`) to ensure compatability with different brokers.
- **Position Protection (Auto Break-Even)**: Scans open trades and automatically moves the stop loss (SL) to the entry price (+ buffer) once the trade gets close to the target Take Profit level.

---

## Project Structure

- `listener.py`: The entry point script. Connects to Telegram and runs background threads for monitoring positions and signals.
- `parser.py`: Extracts trade details (Action, Entry Range, SL, TP) from text messages.
- `signal_manager.py`: Manages the active signals list in `active_signals.json`.
- `signal_monitor.py`: Polls live market price updates to execute trades when entry zones are hit.
- `mt5_executor.py`: Interacts with MetaTrader 5 API to execute orders.
- `position_manager.py`: Implements trailing break-even logic for open positions.
- `get_group_id.py` / `telegram_test.py`: Utility scripts to get Telegram channel or group IDs.
- `mt5_test.py`: Connection check utility for MetaTrader 5.

---

## Prerequisites

### 1. Windows OS
The `MetaTrader5` Python library is natively supported only on **Windows**.

### 2. MetaTrader 5 Terminal
- Install the **MetaTrader 5 Desktop Terminal**.
- Log in to your demo or live broker account.
- **Enable Algorithmic Trading**:
  1. In MT5, go to `Tools` -> `Options` -> `Expert Advisors`.
  2. Check `Allow Algorithmic Trading`.
  3. Keep the MT5 terminal running while the bot is active.

### 3. Telegram API Credentials
- Go to [my.telegram.org](https://my.telegram.org) and log in.
- Navigate to **API development tools** and create an application to get your `api_id` and `api_hash`.

---

## Installation & Setup

1. **Clone or download** this repository.
2. **Install dependencies** using `pip`:
   ```bash
   pip install telethon MetaTrader5
   ```
3. **Configure Telegram API**:
   Open `listener.py` and replace the details with your own credentials:
   ```python
   api_id = 12345678          # Replace with your Telegram API ID (integer)
   api_hash = "your_api_hash" # Replace with your Telegram API Hash (string)
   ```

---

## How to Run (Step-by-Step)

### Step 1: Find your Target Telegram Group/Channel ID
1. Run `get_group_id.py` in your terminal:
   ```bash
   python get_group_id.py
   ```
2. During the first run, Telethon will prompt you to enter your **Telegram Phone Number** and the **Login Code** sent to your Telegram app. This generates a secure session file `session_hanif.session` so you won't need to log in again.
3. The script will list all your chat dialogs and their corresponding IDs. Look for the signal group/channel and copy its numeric ID.
4. Paste this ID into `listener.py`:
   ```python
   GROUP_ID = -100xxxxxxxxxx  # Replace with your target Telegram Group/Channel ID
   ```

### Step 2: Test your MT5 Connection
1. Open your MT5 Terminal application.
2. Run the connection test script:
   ```bash
   python mt5_test.py
   ```
3. If successful, you will see your MT5 account details printed in the terminal.

### Step 3: Run the Auto-Trader Bot
1. Keep the MT5 Terminal open.
2. Start the listener bot:
   ```bash
   python listener.py
   ```
3. The bot will print `BOT LIVE TRADING READY...` and start listening for signals.

---

## Signal Format Example
The parser currently reads signals formatted like:
```text
GOLD BUY NOW @ 1800-1805
SL 1795
TP 1810
TP 1820
```
- It will parse this as a `BUY` signal for `XAUUSD` with an entry range of `1800` to `1805`, stop loss of `1795`, and take profit levels.
