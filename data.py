import yfinance as yf

def get_history(stock_name, period = None, interval = "1d", auto_adjust = True, group_by = 'ticker', progress = False):
    dat = yf.Tickers(stock_name)

    if len(stock_name.split(",")) > 1:
        result_tickers =  dat.history(
            period = period,
            interval = interval,
            auto_adjust = auto_adjust,
            group_by = group_by,
            progress = progress
            )
        result = result_tickers
    else:
        result_ticker =  yf.Ticker(stock_name).history(
            period = period,
            interval = interval,
            auto_adjust = auto_adjust
            )
        result = result_ticker

    if result is None or result.empty:#checking if the dataframe is empty
        return None
    else:
        return result

def save_data(df, file_name):
    df.to_csv(file_name)
    print(f"The data you requested is saved in {file_name}")