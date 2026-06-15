import json
import os
import threading
import time
import uuid

FILE_NAME = "active_signals.json"
file_lock = threading.RLock()


def load_signals():
    with file_lock:
        if not os.path.exists(FILE_NAME):
            return []
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading signals: {e}")
            return []


def save_signals(signals):
    with file_lock:
        try:
            with open(FILE_NAME, "w") as f:
                json.dump(signals, f, indent=4)
        except Exception as e:
            print(f"Error saving signals: {e}")


def signals_match(s1, s2):
    if "id" in s1 and "id" in s2:
        return s1["id"] == s2["id"]
    return (
        s1.get("symbol") == s2.get("symbol")
        and s1.get("action") == s2.get("action")
        and s1.get("entry_min") == s2.get("entry_min")
        and s1.get("entry_max") == s2.get("entry_max")
        and s1.get("sl") == s2.get("sl")
    )


def add_signal(signal):
    with file_lock:
        signals = load_signals()

        # anti duplicate
        for s in signals:
            if (
                s.get("symbol") == signal.get("symbol")
                and s.get("action") == signal.get("action")
                and s.get("entry_min") == signal.get("entry_min")
                and s.get("entry_max") == signal.get("entry_max")
                and s.get("sl") == signal.get("sl")
            ):
                print("SIGNAL SUDAH ADA")
                return

        signal["status"] = "WAITING"
        signal["id"] = str(uuid.uuid4())

        signals.append(signal)
        save_signals(signals)

        print("SIGNAL DISIMPAN")


def update_signal(signal):
    with file_lock:
        signals = load_signals()

        if signal.get("status") in ("EXPIRED", "EXECUTED") and "updated_at" not in signal:
            signal["updated_at"] = time.time()

        updated = False
        for i, s in enumerate(signals):
            if signals_match(s, signal):
                signals[i] = signal
                updated = True
                break

        if updated:
            save_signals(signals)
        else:
            print("SIGNAL UNABLE TO UPDATE (NOT FOUND)")


def clean_signals():
    with file_lock:
        signals = load_signals()
        current_time = time.time()
        new_signals = []
        updated = False

        for s in signals:
            status = s.get("status")
            if status in ("EXPIRED", "EXECUTED"):
                if "updated_at" not in s:
                    s["updated_at"] = current_time
                    new_signals.append(s)
                    updated = True
                else:
                    elapsed = current_time - s["updated_at"]
                    if elapsed < 60:
                        new_signals.append(s)
                    else:
                        updated = True
                        print(f"SIGNAL DELETED (Expired/Executed for > 1 min): {s.get('symbol')} {s.get('action')}")
            else:
                new_signals.append(s)

        if updated:
            save_signals(new_signals)