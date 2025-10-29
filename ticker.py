import yfinance as yf

def ticker(stock_name):

#Keys to print from info dictionary
    fields = [
    "previousClose",
    "open",
    "dayLow",
    "dayHigh",
    "fiftyTwoWeekLow",
    "fiftyTwoWeekHigh",
    "allTimeHigh",
    "allTimeLow",
    "symbol",
    "shortName"
]

    dat = yf.Ticker(stock_name)
    
    for key in fields:
        print(f"{key}: {dat.info[key]}", end = "\n\n")