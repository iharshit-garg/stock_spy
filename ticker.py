import yfinance as yf

class Ticker:
    def __init__(self, stock_name):
            self.stock_name = stock_name
            self.ticker = yf.Ticker(stock_name)

    def tickerInfo(self):
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
            if key in self.ticker.info: #to prevent key error crashes
                print(f"{key.title()}: {self.ticker.info[key]}", end = "\n\n")

    def earningsHistory(self):
        print(self.ticker.earnings_history)

    def assetNews(self):
        print(self.ticker.news)