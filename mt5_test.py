import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 gagal connect")
    quit()

account = mt5.account_info()
print(account)

mt5.shutdown()