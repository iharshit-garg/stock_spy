import yfinance as yf

def get_history(stock_name, period = None, interval = "1d", auto_adjust = True, group_by = 'ticker'):
    dat = yf.Tickers(stock_name)
    return dat.history(
        period = period,
        interval = interval,
        auto_adjust = auto_adjust,
        group_by = group_by
        )

'''
For single ticker, use yf.Ticker(stock_name).history(**args)
'''