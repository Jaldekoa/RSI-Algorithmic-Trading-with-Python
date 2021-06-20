#Importar paquetes
import time
import cbpro
import pandas as pd
import pandas_ta as ta
from functools import reduce

#Generic variables
key = "YOUR API KEY GOES HERE"
b64secret = "YOUR SECRET API KEY GOES HERE"
passphrase = "YOUR PASSPHRASE GOES HERE"

granularity = 86400 #[60 = "1min", 300 = "5min", 900 = "15min", 3600 = "1h", 21600 = "6h", 86400 = "1d"]
short, long = 9, 25 #RSI short and RSI long
fiat = "EUR" #Your fiat currency here, preferably USD or EUR
coins = [fiat, "BTC", "ETH", "BCH", "LTC", "LINK"] #Crypto coins you want to trade

while True:
    try:

        #Authenticated connection with Coinbase
        auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

        #Get the addresses of the crypto coin accounts
        all_accounts = pd.DataFrame(auth_client.get_accounts(),
                                    columns=["id", "currency", "balance", "hold", "available", "profile_id", "trading_enabled"])
        accounts = {fiat: "", "BTC": "", "ETH": "", "BCH": "", "LTC": "", "LINK": ""}
        for i in coins:
            accounts[i] = all_accounts["id"][all_accounts["currency"] == i].values[0]


        #Obtain balance data for each account
        balances = {fiat: 0.0, "BTC": 0.0, "ETH": 0.0, "BCH": 0.0, "LTC": 0.0, "LINK": 0.0}
        for i in coins:
            balances[i] = float(auth_client.get_account(accounts[i])['available'])

        #Obtain historical data for each crypto coin
        df_coins = []
        for i in coins:
            if i != fiat:
                df_coins.append(
                    pd.DataFrame(auth_client.get_product_historic_rates(i + "-" + fiat, granularity=granularity),
                                 columns=["time", "low", "high", "open", i + fiat, "volume"])[["time", i + fiat]])

        #Combine dataframes and format date
        df = reduce(lambda left, right: pd.merge(left, right, on="time"), df_coins)
        df["time"] = pd.to_datetime(df["time"], unit='s')
        df = df.sort_values(by="time", ignore_index=True)

        #Calculate RSI differences (+: buy, -: sell)
        for i in coins:
            if i != fiat:
                df["DifRSI" + i] = ta.rsi(df[i + fiat], length=short) - ta.rsi(df[i + fiat], length=long)

        #Discard the rows with NA
        df = df.dropna()

        #Start of buy-sell orders
        sell_queue = []
        buy_queue = []

        #Sell queue
        for i in coins:
            if i != fiat:
                if df["DifRSI"+i].iloc[-1] < 0.0 and balances[i] > 0.0:
                    sell_queue.append(i)

        #Buy queue
        for i in coins:
            if i != fiat:
                if df["DifRSI"+i].iloc[-1] > 0.0 and balances[fiat] > 0.0:
                    buy_queue.append(i)


        #Sell orders
        for s in sell_queue:
            auth_client.place_market_order(product_id=s+"-"+fiat, side='sell', size=str(balances[s]))

        #Buy orders
        for b in buy_queue:
            auth_client.place_market_order(product_id=b+"-"+fiat, side='buy', funds=str(balances[b]/len(buy_queue)))

        time.sleep(granularity)

    except:
        pass



