import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

_conn = None

def get_connection():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return _conn

def upsert_instrument(symbol: str, name: str = None, asset_class: str = None, exchange: str = None):
    sql = """
        INSERT INTO instruments (symbol, name, asset_class, exchange)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (symbol) DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (symbol, name, asset_class, exchange))
        conn.commit()

def upsert_bars(df, symbol: str, timespan: str = "day"):
    rows = [
    (
        symbol, 
        index, timespan, 
        float(row["Open"]),
        float(row["High"]), 
        float(row["Low"]), 
        float(row["Close"]), 
        float(row["Volume"])
    )
    for index, row in df.iterrows()
    ]

    sql = """
        INSERT INTO ohlcv_bars (symbol, timestamp, timespan, open, high, low, close, volume)
        VALUES %s
        ON CONFLICT (symbol, timestamp, timespan) DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, rows)
        conn.commit()

def get_bars(symbol: str, start: str, end: str, timespan: str = "day") -> pd.DataFrame:
    sql = """
        SELECT timestamp, open, high, low, close, volume
        FROM ohlcv_bars
        WHERE symbol = %s
            AND timespan = %s
            AND timestamp >= %s
            AND timestamp <= %s
        ORDER BY timestamp ASC;
        """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (symbol, timespan, start, end))
            rows = cur.fetchall()
        
    if not rows:
        return None
    
    df = pd.DataFrame(rows, columns = ["Date", "Open", "High", "Low", "Close", "Volume"])
    df = df.set_index("Date").sort_index(ascending = True)
    return df

def save_risk_snapshot(symbol: str, stats_dict: dict, period_start: str, period_end: str):
    sql = """
        INSERT INTO risk_snapshots
            (symbol, period_start, period_end, volatility, annualized_volatility, max_drawdown, sharpe_ratio)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, computed_at) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                symbol,
                period_start,
                period_end,
                stats_dict["volatility"],
                stats_dict["annualized_volatility"],
                stats_dict["max_drawdown"],
                stats_dict["sharpe_ratio"],
            ))
        conn.commit()

def save_anomalies(result: pdf.DataFrame, symbol: str):
    flagged = result[result["rule_flagged"] & result["iso_flagged"] == True] #only saving high confidence anomalies

    if flagged.empty:
        print("No anomalies to save.")

    rows = [
        (
            symbol, 
            index.to_pydatetime(),
            float(row["daily_return"]),
            float(row["volume_ratio"]),
            float(row["price_gap"]),
            float(row["hl_range"]),
            float(row["return_zscore"]),
            float(row["iso_score"]),
            bool(row["rule_flagged"]),
            bool(row["iso_flagged"]),
            bool(row["anomaly"]),
        )
        for index, row in flagged.iterrows()
    ]
    sql  = """
        INSERT INTO anomaly_flags (
        symbol, timestamp, daily_return, volume_ratio, price_gap, hl_range, return_zscore,
        iso_score, rule_flagged, iso_flagged, anomaly
    )
    VALUES %s
    ON CONFLICT (symbol, timestamp) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, rows)
        conn.commit()
    
    print(f"💾 {len(rows)} anomaly flag(s) saved to database.")


if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")