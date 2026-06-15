import MetaTrader5 as mt5

# ==================================
# INIT MT5
# ==================================
if not mt5.initialize():
    print("MT5 initialize failed")

SYMBOL_MAP = {
    "GOLD": "XAUUSD",
    "XAUUSD": "XAUUSD"
}

# ==================================
# FILLING MODE FALLBACK
# ==================================
FILLING_MODES = [
    mt5.ORDER_FILLING_FOK,
    mt5.ORDER_FILLING_RETURN,
    mt5.ORDER_FILLING_IOC
]


# ==================================
# SYMBOL MAPPING
# ==================================
def get_symbol(symbol):
    return SYMBOL_MAP.get(symbol, symbol)


# ==================================
# MARKET CHECK
# ==================================
def is_market_open(symbol):
    info = mt5.symbol_info(symbol)

    if info is None:
        return False

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return False

    if tick.bid == 0 or tick.ask == 0:
        return False

    return True


# ==================================
# ENTRY ZONE CHECK
# ==================================
def is_inside_entry_zone(current_price, entry_min, entry_max):
    return entry_min <= current_price <= entry_max


# ==================================
# SIGNAL VALIDATION
# ==================================
def validate_signal(action, price, sl, tp):
    if action == "BUY":

        if sl >= price:
            return False, "SL harus di bawah harga BUY"

        if tp <= price:
            return False, "TP harus di atas harga BUY"

    elif action == "SELL":

        if sl <= price:
            return False, "SL harus di atas harga SELL"

        if tp >= price:
            return False, "TP harus di bawah harga SELL"

    return True, "OK"


# ==================================
# SEND ORDER WITH FALLBACK
# ==================================
def send_order_with_fallback(request):

    last_result = None

    for mode in FILLING_MODES:

        request["type_filling"] = mode

        result = mt5.order_send(request)

        print(
            f"TRY MODE {mode} -> "
            f"RETCODE {result.retcode if result else None}"
        )

        last_result = result

        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"SUCCESS MODE {mode}")
            return result

    return last_result


# ==================================
# OPEN TRADE
# ==================================
def open_trade(signal):

    try:

        symbol = get_symbol(signal["symbol"])

        action = signal["action"]

        entry_min = signal["entry_min"]
        entry_max = signal["entry_max"]

        sl = signal["sl"]

        tp = signal["tp"][0]  # TP1 only

        if not mt5.initialize():
            print("MT5 initialize failed")
            return None

        if not is_market_open(symbol):
            print("MARKET CLOSED / NO QUOTE")
            return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print("NO TICK DATA")
            return None

        # BUY pakai ASK
        # SELL pakai BID
        price = tick.ask if action == "BUY" else tick.bid

        print(
            f"HARGA SEKARANG = {price} | "
            f"ENTRY ZONE = {entry_min}-{entry_max}"
        )

        # ==================================
        # ENTRY ZONE FILTER
        # ==================================
        if not is_inside_entry_zone(
            price,
            entry_min,
            entry_max
        ):
            print(
                f"SKIP TRADE: Harga {price} "
                f"di luar zona "
                f"{entry_min}-{entry_max}"
            )
            return None

        # ==================================
        # VALIDASI SL / TP
        # ==================================
        valid, msg = validate_signal(
            action,
            price,
            sl,
            tp
        )

        if not valid:
            print("SKIP TRADE:", msg)
            return None

        # ==================================
        # FIXED LOT
        # ==================================
        lot = 0.01

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY
            if action == "BUY"
            else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 2026,
            "comment": "TG BOT FIXED 0.01",
            "type_time": mt5.ORDER_TIME_GTC
        }

        result = send_order_with_fallback(request)

        print("\nORDER RESULT:")
        print(result)

        return result

    except Exception as e:
        print("OPEN TRADE ERROR:", e)
        return None