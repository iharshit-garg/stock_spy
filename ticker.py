import yfinance as yf

class Ticker:
    def __init__(self, stock_name):
            self.stock_name = stock_name
            self.dat = yf.Ticker(stock_name)

    def tickerInfo(stock_name):
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
        
        for key in fields:
            print(f"{key.title()}: {self.dat.info[key]}", end = "\n\n")

    def earningsHistory(stock_name):
        print(dat.earnings_history)

    def assetNews(stock_name):
        print(dat.news)