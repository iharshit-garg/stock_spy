import yfinance as yf

def get_history(stock_name, period = None, interval = "1d", auto_adjust = True, group_by = 'column'):
    dat = yf.Tickers(stock_name)
    return dat.history(period, interval, auto_adjust, group_by)