import yfinance as yf

def ticker(stock_name):

#Keys to print from info dictionary
    fields = [
    "symbol",
    "shortName",
    "previousClose",
    "open",
    "dayLow",
    "dayHigh",
    "fiftyTwoWeekLow",
    "fiftyTwoWeekHigh",
    "allTimeHigh",
    "allTimeLow",
]

    dat = yf.Ticker(stock_name)
    
    for key in fields:
        print(f"{key.title()}: {dat.info[key]}", end = "\n\n")

def earningsHistory(stock_name):
    dat = yf.Ticker(stock_name)
    print(dat.earnings_history)

def assetNews(stock_name):
    dat = yf.Ticker(stock_name)
    print(dat.news)