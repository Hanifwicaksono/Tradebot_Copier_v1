import MetaTrader5 as mt5
import time


# =========================
# BEP WHEN NEAR TP
# =========================
def move_be_when_near_tp(symbol, position, near_tp_pips=10, buffer_pips=1):
    tick = mt5.symbol_info_tick(symbol)
    info = mt5.symbol_info(symbol)

    if tick is None or info is None:
        return None

    point = info.point

    entry = position.price_open
    tp = position.tp
    sl = position.sl

    # skip kalau TP tidak ada
    if tp is None or tp == 0:
        return None

    # harga sekarang
    current_price = tick.bid if position.type == 0 else tick.ask

    # =========================
    # BUY POSITION
    # =========================
    if position.type == 0:
        distance_to_tp = (tp - current_price) / point

        # belum dekat TP
        if distance_to_tp > near_tp_pips:
            return None

        new_sl = entry + (buffer_pips * point)

        # jangan downgrade SL
        if sl is not None and sl >= new_sl:
            return None

    # =========================
    # SELL POSITION
    # =========================
    else:
        distance_to_tp = (current_price - tp) / point

        # belum dekat TP
        if distance_to_tp > near_tp_pips:
            return None

        new_sl = entry - (buffer_pips * point)

        # jangan downgrade SL
        if sl is not None and sl <= new_sl:
            return None

    # =========================
    # SEND MODIFY REQUEST
    # =========================
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": position.ticket,
        "symbol": symbol,
        "sl": new_sl,
        "tp": tp
    }

    result = mt5.order_send(request)

    print(f"[BEP NEAR TP] ticket={position.ticket} result={result}")
    return result


# =========================
# MONITOR LOOP
# =========================
def monitor_positions(interval=5):
    while True:
        positions = mt5.positions_get()

        if positions:
            for pos in positions:
                move_be_when_near_tp(pos.symbol, pos)

        time.sleep(interval)