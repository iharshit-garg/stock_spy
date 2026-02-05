import yfinance as yf

def get_history(stock_name, period = None, interval = "1d", auto_adjust = True, group_by = 'ticker', progress = False):
    dat = yf.Tickers(stock_name)
    result =  dat.history(
        period = period,
        interval = interval,
        auto_adjust = auto_adjust,
        group_by = group_by,
        progress = progress
        )
    if result is None or result.empty:#checking if the dataframe is empty
        return None
    else:
        return result
'''
For single ticker, use yf.Ticker(stock_name).history(**args)
'''