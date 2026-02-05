import yfinance as yf

class Ticker:
    def __init__(self, stock_name):
            self.stock_name = stock_name
            self.ticker = yf.Ticker(stock_name)

    def get_basic_info(self): #return dict
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
        
        result = {}
        for key in fields:
             result[key] = self.ticker.info.get(key, None) #using get() method to prevent key error crashes
        return result