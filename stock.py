import yfinance as y

def stock(stock_name):

    dat = yf.Ticker(stock_name)
    
    print(dat.info.keys())