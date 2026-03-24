import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

_conn = None

def get_connection():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return _conn

def create_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS instruments (
        symbol       VARCHAR PRIMARY KEY,
        name         VARCHAR,
        asset_class  VARCHAR,
        exchange     VARCHAR,
        created_at   TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS ohlcv_bars (
        symbol      VARCHAR NOT NULL REFERENCES instruments(symbol),
        timestamp   TIMESTAMPTZ NOT NULL,
        timespan    VARCHAR NOT NULL,
        open        NUMERIC(12,4),
        high        NUMERIC(12,4),
        low         NUMERIC(12,4),
        close       NUMERIC(12,4),
        volume      BIGINT,
        PRIMARY KEY (symbol, timestamp, timespan)
    );

    CREATE TABLE IF NOT EXISTS risk_snapshots (
        symbol               VARCHAR NOT NULL REFERENCES instruments(symbol),
        computed_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        period_start         TIMESTAMPTZ,
        period_end           TIMESTAMPTZ,
        volatility           NUMERIC(10,6),
        annualized_volatility NUMERIC(10,6),
        max_drawdown         NUMERIC(10,6),
        sharpe_ratio         NUMERIC(10,6),
        PRIMARY KEY (symbol, computed_at)
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

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
            index,
            timespan,
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            row["volume"],
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

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")