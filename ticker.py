import yfinance as yf

def ticker(stock_name):

    dat = yf.Ticker(stock_name)
    for i in dat.info.keys():
        print(i,end = "\n\n")