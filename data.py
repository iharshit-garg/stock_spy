import yfinance as yf

def get_history(stock_name, period = "1mo", interval = "1d", auto_adjust = True, group_by = 'ticker', progress = False):
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

def stats(df) -> dict[str, float]:
    daily_returns = df['Close'].pct_change().dropna(how = 'all') #selecting column 'Close' and printing daily change decimal values
    
    volatility = daily_returns.std() #selecting column 'Close' and printing standard deviation
    annualized_volatility = volatility*(252**0.5) #printing annual volatility by multiplying by total trading days in a year

    running_peak = df['Close'].cummax()
    drawdown = (df['Close'] - running_peak) / running_peak
    max_drawdown = drawdown.min()

    return {
        "volatility": float(volatility),
        "annualized_volatility": float(annualized_volatility),
        "max_drawdown": float(max_drawdown)
    }