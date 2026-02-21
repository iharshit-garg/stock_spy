# StockSpy

StockSpy is a Python command-line tool to **search**, **inspect**, and **analyze** financial instruments using market data APIs. It is designed as a beginner-friendly but quant-minded project that gradually evolves toward more professional tooling (CLI flags, databases, and better risk metrics).


## Features

### 1. Instrument Lookup

- Search by plain name (e.g., `Apple`, `Nvidia`) and instrument type (`stock`, `etf`, `index`, `cryptocurrency`).
- Display top candidates (symbol + short name).
- Let the user interactively choose the correct symbol.
- Return the chosen symbol to be used by the rest of the tool.

### 2. Basic Ticker Information

- Given a symbol (e.g., `AAPL`), fetch basic metadata:
  - Symbol
  - Short name
  - Previous close
  - Open
  - Day low / day high
  - 52-week low / 52-week high
  - All-time high / all-time low (when available)
- Data is returned as a Python dictionary and then printed by the CLI.

### 3. Historical Price Data

- Fetch historical OHLCV data for a single symbol:
  - Configurable `period` (e.g. `1mo`, `3mo`, `1y`, `max`).
  - Configurable `interval` (e.g. `1d`, `1wk`, `1mo`, or intraday).
- Summary output:
  - Total number of rows.
  - First bar (first timestamp).
  - Last bar (most recent bar).
- Basic price statistics:
  - Highest high over the period.
  - Lowest low over the period.
  - Average closing price over the period.

### 4. Risk & Performance Statistics

Given a DataFrame of historical prices (with at least a `Close` column), the project computes:

- Daily returns using percentage change on close prices.
- **Volatility**: standard deviation of daily returns (in decimal form).
- **Annualized volatility**: daily volatility scaled by \(\sqrt{252}\), representing yearly volatility in decimal form.
- **Max drawdown**: worst peak-to-trough decline, computed from the running maximum of the close price, expressed as a negative decimal (e.g. `-0.35` for -35%).

These statistics are returned as a dictionary and can be extended with more metrics over time (e.g. Sharpe Ratio, Sortino Ratio, CAGR, etc.).

### 5. Data Export (CSV)

- After fetching and summarizing historical data, StockSpy can save the DataFrame to CSV.
- Filenames follow a consistent naming scheme:
  - `<SYMBOL>_<PERIOD>_<INTERVAL>.csv`
- This allows offline analysis and re-use of the same data without refetching from the API.


## Project Structure

A high-level overview of the modules:

- `stockSpy.py`  
  Main CLI entry point. Handles:
  - Menu / user interaction.
  - Symbol lookup or direct symbol input.
  - Routing to:
    - Basic info (`Ticker`).
    - Historical data (`get_history` + summary + stats).
  - Calling `save_data` to export CSVs.

- `lookup.py`  
  Provides `lookup(security_name, instrument_type)`:
  - Uses the API’s lookup/search functionality to retrieve candidates as a DataFrame.
  - Checks if the DataFrame is empty.
  - Displays the top N (e.g. 10) `shortName` entries with their symbols.
  - Lets the user choose a symbol by index and returns the selected symbol.
  - Returns `None` if type is invalid or no results are found.

- `ticker.py`  
  Wraps a single instrument:
  - Initializes a ticker object for a given symbol.
  - `get_basic_info()`:
    - Builds a dictionary from selected fields of the ticker’s `info` dict.
    - Uses `.get()` to avoid key errors when a field is missing.

- `data.py`  
  Historical data layer:
  - `get_history(stock_name, period="1mo", interval="1d", ...)`:
    - For a single symbol: uses `Ticker.history()` to get OHLCV.
    - For multiple symbols: uses a multi-ticker call (prepared for future multi-symbol support).
    - Returns `None` if the resulting DataFrame is empty.
  - `save_data(df, file_name)`:
    - Saves the given DataFrame to a CSV file.
    - Prints the path/name of the saved file to the user.
  - `stats(df)`:
    - Encapsulates calculations like:
        - Daily returns.
        - Volatility and annualized volatility.
        - Max drawdown.
        - Future metrics: Sharpe Ratio, Sortino Ratio, etc.


## Current Workflow

1. Start the program.
2. Choose a menu option:
   - `[1] Basic Info`
   - `[2] Historical Prices`
3. Decide whether you know the symbol:
   - If **no**:
     - Enter a name (`Apple`) and instrument type (`stock`, `etf`, etc.).
     - Use `lookup()` to select the symbol from top results.
   - If **yes**:
     - Enter the symbol directly (`AAPL`, `VOOG`).
4. For **Basic Info**:
   - Fetch and display key ticker fields.
5. For **Historical Prices**:
   - Enter `period` and `interval`.
   - Fetch OHLCV data.
   - If data is found:
     - Print row count, first bar, last bar.
     - Print highest high, lowest low, average close.
     - Compute and print volatility / annualized volatility / max drawdown.
     - Save the full DataFrame to CSV.


## Planned Improvements

The following tasks are planned to evolve StockSpy from a simple educational tool into a more robust and extensible application.

### 1. Replace yfinance with Polygon.io API

- **Goal**: Use Polygon.io as the primary market data provider.
- **Why**:
  - More consistent and reliable data for equities, crypto, and other asset classes.
  - Better suited for intraday and potentially higher-frequency use cases.

### 2. Replace Menu-Based CLI with Argparse

- **Goal**: Turn StockSpy into a script that can be called with flags, e.g.:
  - `python stockSpy.py --info --symbol AAPL`
  - `python stockSpy.py --history --symbol AAPL --period 1y --interval 1d`
- **Why**:
  - Easier automation and integration into other tools or shell scripts.
  - More “Unix-like” and professional interface.

### 3. Replace CSV with PostgreSQL

- **Goal**: Persist price history and statistics in PostgreSQL instead of flat CSV files.
- **Why**:
  - Better queryability (e.g., multi-asset queries, time-window filters, joining with other datasets).
  - More realistic for production-like quant infrastructure.

### 4. Logging

- **Goal**: Add structured logging instead of relying only on `print`.
- **Why**:
  - Easier debugging and introspection.
  - Better separation between user-facing output and developer diagnostics.
- **Tasks**:
  - Introduce a logging setup (levels such as DEBUG, INFO, WARNING, ERROR).

### 5. Fix Variable Naming Scheme

- **Goal**: Enforce a consistent, Pythonic naming convention.
- **Why**:
  - Improves readability and maintainability.
  - Makes the project more approachable for contributors.

### 6. Input Validation for `data_period` & `data_interval`

- **Goal**: Prevent invalid period/interval combinations from reaching the API.
- **Why**:
  - Better user experience: show helpful error messages instead of API error traces.
  - More robust code that fails early and clearly.


## Roadmap Ideas

Beyond the listed issues, possible future enhancements:

- Add more risk/return metrics:
  - Sharpe Ratio, Sortino Ratio, Calmar Ratio, CAGR.
- Implement a watchlist system:
  - Store symbol + threshold rules.
  - Periodically fetch latest prices and trigger alerts (console, email, etc.).
- Add plotting:
  - Basic price charts (Close over time).
  - Overlay moving averages or volatility bands.


## Getting Started

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies (e.g. `yfinance`, `pandas`, and others listed in `requirements.txt`).
4. Run the script:
   - Current mode: interactive CLI.
   - Future mode: argparse-driven CLI with flags and subcommands.