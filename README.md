# RSI Algorithmic Trading with Python

In this repository you can see my first algorithhmic trading script. I use 5 cryptocurrencies: Bitcoin (BTC), Ethereum (ETH), Bitcoin Cash (BCH), Litecoin (LTC) and Chainlink (LINK).

## Trading based on a cross of RSI indicators

The  [Relative Strength Index](https://en.wikipedia.org/wiki/Relative_strength_index) (**RSI**) is a technical indicator used in the analysis of financial markets. It is intended to chart the current and historical strength or weakness of a stock or market based on the closing prices of a recent trading period.

Here I test a method to invest in based on crossing RSI indicators. I set two windows: a short one of 9 periods and a long one based on 25 periods. You can change it easily.

```
short, long = 9, 25
```

The rule to trade is as following:

1. If the short RSI indicator is over the long RSI indicator, it buy the cryptocurrency.
2. If the short RSI indicator is under the long RSI indicator, it sell the cryptocurrency.
3. The weight is allocated equally between every currency that is recommended to buy.
4. If there no currency avalilable to invest, it keep money in cash (fiat currency).

## Periods of time

I recommend using a time interval of 1 day since according to the tests I have carried out, it is the most profitable period due to the exchange's fees (0.5% for maker and taker in market orders).

You can change the base period of time in the next variable:

```
#[60 = "1min", 300 = "5min", 900 = "15min", 3600 = "1h", 21600 = "6h", 86400 = "1d"]
granularity = 60
```
Time expressed in seconds.

## Coinbase Pro API

You must create an API key in [Coinbase Pro](https://pro.coinbase.com/) > Profile > API. You need three different strings:

```
key = "YOUR API KEY GOES HERE"
b64secret = "YOUR SECRET API KEY GOES HERE"
passphrase = "YOUR PASSPHRASE GOES HERE"
```

## Cryptocurrencies and fiat money

You can easily change which cryptos you want the script to trade. You can change your fiat currency too.

```
#Your fiat currency here, preferably USD or EUR
fiat = "EUR"

#Cryptocurrencies you want to trade
coins = [fiat, "BTC", "ETH", "BCH", "LTC", "LINK"]
```

I have tested that the script works with EUR and USD.


## References
***This project is based on the following article:***
- *Automating cryptocurrencies investment: https://quantdare.com/automating-cryptocurrencies-investment/*
