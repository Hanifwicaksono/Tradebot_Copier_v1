import re

def parse_signal(text):
    text = text.upper()

    signal = {
        "symbol": "XAUUSD",
        "action": None,
        "entry_min": None,
        "entry_max": None,
        "sl": None,
        "tp": []
    }

    if "BUY" in text:
        signal["action"] = "BUY"

    elif "SELL" in text:
        signal["action"] = "SELL"

    # ENTRY RANGE
    entry_match = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)', text)

    if entry_match:
        p1 = float(entry_match.group(1))
        p2 = float(entry_match.group(2))

        signal["entry_min"] = min(p1, p2)
        signal["entry_max"] = max(p1, p2)

    # SL
    sl_match = re.search(r'SL\s*(\d+(?:\.\d+)?)', text)

    if sl_match:
        signal["sl"] = float(sl_match.group(1))

    # TP
    tp_matches = re.findall(r'TP\s*(\d+(?:\.\d+)?)', text)

    for tp in tp_matches:
        signal["tp"].append(float(tp))

    return signal