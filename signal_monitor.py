import time
import MetaTrader5 as mt5

from signal_manager import load_signals, update_signal
from mt5_executor import open_trade


def monitor_signals():

    while True:

        signals = load_signals()

        for i, signal in enumerate(signals):

            if signal["status"] != "WAITING":
                continue

            symbol = signal["symbol"]

            tick = mt5.symbol_info_tick(symbol)

            if tick is None:
                continue

            price = tick.ask

            entry_min = signal["entry_min"]
            entry_max = signal["entry_max"]

            tp1 = signal["tp"][0]

            # ======================
            # BUY
            # ======================
            if signal["action"] == "BUY":

                # TP sudah tercapai
                if price >= tp1:

                    signal["status"] = "EXPIRED"
                    update_signal(i, signal)

                    print("SIGNAL EXPIRED (TP SUDAH TERSENTUH)")
                    continue

                # harga masuk zone
                if entry_min <= price <= entry_max:

                    result = open_trade(signal)

                    if result:
                        signal["status"] = "EXECUTED"
                        update_signal(i, signal)

                        print("SIGNAL DIEKSEKUSI")

            # ======================
            # SELL
            # ======================
            else:

                price = tick.bid

                if price <= tp1:

                    signal["status"] = "EXPIRED"
                    update_signal(i, signal)

                    print("SIGNAL EXPIRED (TP SUDAH TERSENTUH)")
                    continue

                if entry_min <= price <= entry_max:

                    result = open_trade(signal)

                    if result:
                        signal["status"] = "EXECUTED"
                        update_signal(i, signal)

                        print("SIGNAL DIEKSEKUSI")

        time.sleep(5)