import requests
import pandas as pd

def getBasicCurrencyInformation(x: str) -> pd.DataFrame:
    response = requests.get("https://bittrex.com/api/v1.1/public/getcurrencies")
    currency_list = pd.DataFrame(response.json()["result"])
    return(currency_list[currency_list.CurrencyLong.str.contains(x)])

def findLowestTxFeeCurrency() -> pd.DataFrame:
    response = requests.get("https://bittrex.com/api/v1.1/public/getcurrencies")
    currency_list = pd.DataFrame(response.json()["result"])
    return(currency_list.sort_values('TxFee'))

def getCurrentMarketPrice(symbol: str) -> pd.DataFrame:
    response = requests.get("https://bittrex.com/api/v1.1/public/getticker",
                 params={"market": "BTC-"+symbol}
                )
    return(pd.DataFrame(response.json()["result"], index=[symbol]))

def get24MarketSummary(symbol: str) -> pd.DataFrame:
    response = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummary",
                            params={"market": "BTC-"+symbol}
                           )
    return(pd.DataFrame(response.json()["result"], index=[symbol]))

def getMarketSummary() -> pd.DataFrame:
    response = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")
    df = pd.DataFrame(response.json()["result"])
    df.index = df.MarketName
    del df['MarketName']
    return df[df.index.str.contains("BTC")]

def getHistoricData(symbol: str) -> pd.DataFrame():
    response = requests.get("https://bittrex.com/Api/v2.0/pub/market/GetTicks",
                            params={"marketName": "BTC-"+symbol,
                                    "tickInterval": "thirtyMin"
                                   }
                           )
    df = pd.DataFrame(response.json()["result"])
    df["T"] = pd.to_datetime(df["T"])
    return(df)

def getHistoricDataLong(symbol: str) -> pd.DataFrame():
    response = requests.get("https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=BTC&limit=2000&aggregate=1".format(symbol))
    df = pd.DataFrame(response.json()["Data"])
    df["time"] = pd.to_datetime(df["time"],unit="s")
    return(df)

def getCurrentBTCPrice() -> float:
    response = requests.get("https://bittrex.com/Api/v2.0/pub/currencies/GetBTCPrice")
    return response.json()["result"]["bpi"]["USD"]["rate_float"]

crypo_compare_conversion = pd.read_excel("CryptoCompare_NameToTicker.xlsx")
def getCryptoCompareSymbol(coinName: str) -> str:
    direct = crypo_compare_conversion[crypo_compare_conversion.CoinName == coinName]
    if len(direct) == 1:
        return direct["Symbol"].values[0]
    else:
        match = crypo_compare_conversion[crypo_compare_conversion.CoinName.str.contains(coinName, case=False)]["Symbol"].values[0]
        if len(match) > 1:
            raise Exception('Multiple values for CoinName: {} are found'.format(coinName))
        elif len(match) < 1:
            raise Exception('No values were found for CoinName: {}'.format(coinName))
        else:
            return match["Symbol"].values[0]