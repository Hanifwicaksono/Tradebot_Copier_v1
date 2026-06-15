import json
import os

FILE_NAME = "active_signals.json"


def load_signals():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_signals(signals):
    with open(FILE_NAME, "w") as f:
        json.dump(signals, f, indent=4)


def add_signal(signal):
    signals = load_signals()

    # anti duplicate
    for s in signals:
        if (
            s["action"] == signal["action"]
            and s["entry_min"] == signal["entry_min"]
            and s["entry_max"] == signal["entry_max"]
            and s["sl"] == signal["sl"]
        ):
            print("SIGNAL SUDAH ADA")
            return

    signal["status"] = "WAITING"

    signals.append(signal)
    save_signals(signals)

    print("SIGNAL DISIMPAN")


def update_signal(index, signal):
    signals = load_signals()

    signals[index] = signal

    save_signals(signals)