from stockspy.data import get_history, save_data, stats
from stockspy.db import upsert_instrument, save_risk_snapshot
from stockspy.lookup import lookup
from stockspy.ticker import Ticker
from stockspy.anomaly import detect_anomalies
import argparse, sys, time, os
from typing import List

def resolve_symbol(symbol = None, name = None) -> List:
    if symbol:
        if len(symbol.split(",")) > 1:
            multi_tickers = [s.strip().upper() for s in symbol.split(",")]
            return multi_tickers
        else:
            return [symbol.upper()]
    elif name:
        result = lookup(name.lower())
        if result:
            return [result.upper()]
        else:
            sys.exit("Symbol not found!")
    else:
        sys.exit("Error: Must provide either --symbol or --name")

def get_basic_info(args):
    symbol = resolve_symbol(symbol = args.symbol, name = args.name)
    #checking for multi-ticker
    for i in range(len(symbol)):
        print(f"\n⏳ Fetching data for '{symbol[i]}'\n")
        if i > 0:
            time.sleep(12) #to prevent rate limiting, wait 12 seconds

        #calling ticker class
        ticker_instance = Ticker(symbol[i])
        data = ticker_instance.get_basic_info()
        print(f"{symbol[i]}: ✅ fetched")
        for k, v in data.items():
            print(f"{k}: {v}")

def get_historical_data(args):
    symbol = resolve_symbol(symbol = args.symbol, name = args.name)
    #checking for multi-ticker
    for i in range(len(symbol)):
        print(f"\n⏳ Fetching historical data for '{symbol[i]}'\n")
        if i > 0:
            time.sleep(12) #to prevent rate limiting, wait 12 seconds

        #calling get_history
        hist_data = get_history(stock_name = symbol[i], timespan = args.timespan, from_date = args.start, to_date = args.end, multiplier = args.multiplier)
        
        #if function return None, show error
        if hist_data is None :
            print(f"No data found for {symbol[i]}")
            continue
        else:
            print(f"First bar:\n\n{hist_data.head(1)}\n")
            print(f"Last bar:\n\n{hist_data.tail(1)}\n")
            print(f"Highest High: {hist_data["High"].max()}")
            print(f"Lowest Low: {hist_data["Low"].min()}")
            print(f"Average Close: {hist_data["Close"].mean()}")
            
            #volatility, annualized volatility, and max drawdown
            risk_stats = stats(hist_data)
            percentage_fields = {"volatility", "annualized_volatility", "max_drawdown"}
            for k, v in risk_stats.items():
                if k in percentage_fields:
                    print(f"{k}: {v:.2%}")
                else:
                    if k == "sharpe_ratio":
                        print(f"{k}: {v:.2f}")
                    else:
                        print(f"{k}: {v}")

            #saving data
            print("\n📁 Saving data...\n")
            time.sleep(3)

            #save to csv
            if args.save_csv == True:
                folder = "./data"
                os.makedirs(folder, exist_ok = True) #ensure the folder exists
                file = f"{symbol[i]}_{args.start}_{args.end}_{args.timespan}.csv"
                file_path = os.path.join(folder, file)
                save_data(df = hist_data, symbol = symbol[i], export_csv = args.save_csv, csv_path = file_path)

            #save to db
            else:
                upsert_instrument(symbol[i])
                save_data(hist_data, symbol[i], timespan = args.timespan, export_csv = args.save_csv)
                save_risk_snapshot(symbol[i], risk_stats, args.start, args.end)

def get_anomalies(args):
    print(f"\n⏳ Fetching data for '{args.symbol}'\n")
    df = get_history(args.symbol, args.start, args.end)

    if df is None:
        sys.exit(f"No data found for {args.symbol}")

    result = detect_anomalies(df, contamination=args.contamination)

    flagged = result[result["rule_flagged"] & result["iso_flagged"] ] 

    print(f"📊 Analyzed {len(result)} trading days")
    print(f"🚨 High Confidence Anomalies: {len(flagged)}\n")

    if flagged.empty:
        print("No anomalies found.")
        return

    print(flagged[["daily_return", "volume_ratio", "price_gap", "iso_score"]])

def main():
    parser = argparse.ArgumentParser(
        prog = "stockSpy",
        description = "Stock market research CLI"
    )
    subparsers = parser.add_subparsers(
        dest = "command",
        help = "Available commands",
        required = True
    )

    #basic info command
    basic_parser = subparsers.add_parser("info", help = "Fetch basic stock information")
    basic_parser.add_argument("--symbol", type = str, help = "Stock symbol (e.g. AAPL)")
    basic_parser.add_argument("--name", type = str, help = "Stock name (e.g. Apple)")
    basic_parser.set_defaults(func = get_basic_info)
 
    #historical-data
    history_parser = subparsers.add_parser("history", help = "Fetch historical information")
    history_parser.add_argument("--symbol", type = str, help = "Stock symbol (e.g. AAPL)")
    history_parser.add_argument("--name", type = str, help = "Stock name (e.g. Apple)")
    history_parser.add_argument("--timespan", default = "day", type = str, help = "(Optional) Available options: [second, minute, hour, day, week, month, quarter, year]")
    history_parser.add_argument("--multiplier", default = 1, type = int, help = "(Optional) The size of the timespan multiplier")
    history_parser.add_argument("--start", type = str, required = True, help = "Format: [YYYY-MM-DD]")
    history_parser.add_argument("--end", type = str, required = True, help = "Format: [YYYY-MM-DD]")
    history_parser.add_argument("--save_csv", action = "store_true", default = False, help = "Export fetched data to a CSV file")
    history_parser.set_defaults(func = get_historical_data)

    #anomaly detection
    # In main(), add alongside history_parser:
    anomaly_parser = subparsers.add_parser("anomaly", help="Detect anomalies in price data")
    anomaly_parser.add_argument("--symbol", type=str, required=True)
    anomaly_parser.add_argument("--start",  type=str, required=True)
    anomaly_parser.add_argument("--end",    type=str, required=True)
    anomaly_parser.add_argument("--contamination", type=float, default=0.05)
    anomaly_parser.set_defaults(func=get_anomalies)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()