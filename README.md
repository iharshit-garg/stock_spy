# StockSpy

A Python CLI for fetching, storing, and analyzing financial market data — with built-in anomaly detection for flagging unusual price and volume behavior.

Built on Polygon.io for market data, PostgreSQL for persistence, and scikit-learn's Isolation Forest for anomaly scoring.

## Features

- **Instrument lookup** — search by company name, select from top results interactively
- **Basic ticker info** — symbol metadata, previous close, day range, 52-week range via yfinance
- **Historical OHLCV** — fetch daily, hourly, or minute bars via Polygon.io with multi-ticker support
- **Risk & performance stats** — volatility, annualized volatility, max drawdown, Sharpe ratio
- **PostgreSQL persistence** — all bars and risk snapshots stored; no re-fetching the same data twice
- **Anomaly detection** — rule-based (Z-score, volume spike, price gap) + Isolation Forest scoring
- **Optional CSV export** — export any fetch to a timestamped CSV with `--export-csv`

## Tech Stack

| Layer | Tool |
|---|---|
| Market data (OHLCV) | Polygon.io REST API (`polygon-api-client`) |
| Ticker metadata | yfinance |
| Database | PostgreSQL + psycopg2 |
| Schema migrations | Alembic |
| Anomaly detection | scikit-learn `IsolationForest`, pandas rolling stats |
| CLI | argparse |
| Environment config | python-dotenv |

## Project Structure

```
stock_spy/
├── stockspy/
│   ├── client.py       # Polygon.io REST client singleton
│   ├── data.py         # get_history(), save_data(), stats()
│   ├── db.py           # PostgreSQL connection, upsert_bars(), get_bars(), save_risk_snapshot(), save_anomalies(), upsert_instrument()
│   ├── lookup.py       # Interactive symbol search via Polygon.io
│   ├── ticker.py       # Basic ticker metadata via yfinance
│   └── anomaly.py      # Feature engineering, rule-based flags, Isolation Forest scorer
│
├── fraud_detector/     # Planned extension — order matching + fraud scoring
│
├── migrations/         # Alembic migration scripts
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── test_data.py
│   ├── test_db.py
│   ├── test_lookup.py
│   ├── test_ticker.py
│   └── test_anomaly.py
│
├── stockSpy.py         # CLI entry point
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── .env                # API keys and DB URL (not committed)
```

## Database Schema

Four tables managed via Alembic migrations:

**`instruments`** — one row per symbol, reference table for all price data

**`ohlcv_bars`** — historical OHLCV bars with composite primary key `(symbol, timestamp, timespan)`, preventing duplicate inserts on re-fetch

**`risk_snapshots`** — computed stats (volatility, Sharpe, drawdown) persisted per symbol per fetch window

**`anomaly_flags`** — flagged bars with feature values, Isolation  Forest score, rule and model flag columns, and `detected_at` timestamp. Composite Primary key `(symbol, timestamp)`

```sql
-- Example: rank symbols by Sharpe ratio across a period
SELECT symbol, period_start, period_end, sharpe_ratio, max_drawdown
FROM risk_snapshots
ORDER BY sharpe_ratio DESC;
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/iharshit-garg/stock_spy.git
cd stock_spy
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
API_KEY=your_polygon_io_api_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/stockspy
```

Get a free Polygon.io API key at [polygon.io](https://polygon.io).

### 5. Start PostgreSQL

```bash
docker run -d --name stockspy-db \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:16
```

### 6. Run migrations

```bash
alembic upgrade head
```

## Usage

### Fetch basic ticker info

```bash
# By symbol
python stockSpy.py info --symbol AAPL

# By name (interactive search)
python stockSpy.py info --name "Apple"
```

### Fetch historical data

```bash
# Daily bars, single ticker
python stockSpy.py history --symbol AAPL --start 2024-01-01 --end 2024-12-31

# Hourly bars
python stockSpy.py history --symbol TSLA --start 2024-06-01 --end 2024-12-31 \
  --timespan hour --multiplier 1

# Multi-ticker (rate-limit handled automatically)
python stockSpy.py history --symbol AAPL,MSFT,NVDA --start 2024-01-01 --end 2024-12-31

# Also export to CSV
python stockSpy.py history --symbol AAPL --start 2024-01-01 --end 2024-12-31 --export-csv
```

### Anomaly detection

```bash
python stockSpy.py anomaly --symbol AAPL --start 2024-01-01 --end 2025-12-31
```

Example output:

```
⏳ Fetching data for 'AAPL'

📊 Analyzed 415 trading days
🚨 Anomalies detected: 21

                     daily_return  volume_ratio  price_gap  iso_score  rule_flagged  iso_flagged
Date
2025-04-03 04:00:00     -0.092456      1.823617  -0.081960  -0.174535          True         True
2025-04-09 04:00:00      0.153288      2.341022   0.067070  -0.225843          True         True
2025-08-06 04:00:00      0.050907      1.102341   0.013210  -0.071325         False         True
```

Days where both `rule_flagged` and `iso_flagged` are `True` are highest-confidence anomalies confirmed by two independent methods.

## CLI Reference

### `info`

| Argument | Required | Description |
|---|---|---|
| `--symbol` | One of these | Ticker symbol (e.g. `AAPL`) |
| `--name` | One of these | Company name — triggers interactive lookup |

### `history`

| Argument | Required | Default | Description |
|---|---|---|---|
| `--symbol` | One of these | — | Ticker symbol, comma-separated for multi |
| `--name` | One of these | — | Company name — triggers interactive lookup |
| `--start` | Yes | — | Start date `YYYY-MM-DD` |
| `--end` | Yes | — | End date `YYYY-MM-DD` |
| `--timespan` | No | `day` | Bar size: `second / minute / hour / day / week / month` |
| `--multiplier` | No | `1` | Timespan multiplier (e.g. `4` for 4-hour bars) |
| `--export-csv` | No | `False` | Also export fetched data to `./data/` |

### `anomaly`

| Argument | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | — | Ticker symbol |
| `--start` | Yes | — | Start date `YYYY-MM-DD` |
| `--end` | Yes | — | End date `YYYY-MM-DD` |
| `--contamination` | No | `0.05` | Isolation Forest contamination rate (0.01–0.10) |


## Anomaly Detection

Two independent detection layers run on every `anomaly` command:

**Rule-based (explicit thresholds)**
| Rule | Signal | Default Threshold |
|---|---|---|
| Return Z-score | Daily return vs rolling 20-day mean/std | `\|z\| > 3.0` |
| Volume spike | Today's volume vs 20-day average | `> 3.0x` |
| Price gap | Overnight open vs prior close | `\|gap\| > 2%` |

**Model-based (Isolation Forest)**

Five engineered features fed to `IsolationForest`:
- Daily return
- Volume ratio (vs 20-day rolling mean)
- Overnight price gap
- Intraday high-low range normalized by close
- Rolling 20-day return Z-score

Features are standardized with `StandardScaler` before fitting. The model flags the `contamination` fraction of days as anomalous based on multi-feature isolation depth. Days flagged by both layers are highest-confidence anomalies.

## Data Sources & Limitations

- **Polygon.io free tier**: 5 requests/minute, 15-minute delayed quotes, ~2 years of history. Multi-ticker requests are throttled automatically with a 12-second sleep between symbols.
- **yfinance**: Used only for `info` command metadata. No API key required but subject to Yahoo Finance availability.

## Roadmap

### Planned
- [ ] **Fraud Detector extension** — order matching engine + synthetic transaction pipeline + fraud scoring layer reusing the anomaly engine
- [ ] **Backtesting engine** — vectorized signal → position → PnL simulation with Sharpe, CAGR, equity curve output
- [ ] **Watchlist + alerts** — scheduled polling with Slack/Discord webhook notifications
- [ ] **Logging** — replace `print` with structured `logging` (DEBUG/INFO/WARNING/ERROR)
- [ ] **Visualizations** — price charts with anomaly overlays via `matplotlib`/`plotly`

### Done ✅
- [x] Anomaly flags persisted to anomaly_flags table via save_anomalies()
- [x] Alembic migration for anomaly_flags table
- [x] Polygon.io REST API integration (lookup + OHLCV)
- [x] yfinance hybrid for ticker metadata
- [x] argparse subcommand CLI (`info`, `history`, `anomaly`)
- [x] PostgreSQL schema with Alembic migrations
- [x] `ohlcv_bars` + `instruments` + `risk_snapshots` tables
- [x] `ON CONFLICT DO NOTHING` deduplication on re-fetch
- [x] Risk stats: volatility, annualized volatility, max drawdown, Sharpe ratio
- [x] Auto-persist risk snapshots per fetch window
- [x] Multi-ticker support with rate-limit handling
- [x] Rule-based anomaly detection (Z-score, volume spike, price gap)
- [x] Isolation Forest anomaly scoring with StandardScaler
- [x] Optional CSV export with `--export-csv`