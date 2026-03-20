from client import client
import pandas as pd

def get_history(stock_name: str, from_date, to_date, timespan = "day", multiplier = 1) -> pd.DataFrame:
    aggs = []
    for a in client.list_aggs(
        ticker = stock_name,
        timespan = timespan,
        from_ = from_date,
        to = to_date,
        adjusted = True,
        sort = "asc",
        multiplier = multiplier
    ):
        aggs.append(a)

    #if aggs is not empty, create a list of dictionaries
    data = []        
    if aggs:
        for a in aggs:
            data.append({
                'Date': pd.to_datetime(a.timestamp, unit = 'ms'),
                'Open': a.open,
                'High': a.high,
                'Low': a.low,
                'Close': a.close,
                'Volume': a.volume
            })
        #creating data frame
        df = pd.DataFrame(data)
        df = df.set_index('Date').sort_index(ascending = True)
        return df
    
    else:
        return None

def save_data(df, file_name):
    df.to_csv(file_name)
    print(f"The data you requested is saved in {file_name}\n")

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