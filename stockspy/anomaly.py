import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def build_features(df) -> pd.DataFrame:
    features = df.copy()

    #captures unusual price moves
    features["daily_return"] = df["Close"].pct_change()

    #Compare's today's volume to the 20-day average
    features["volume_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()

    #Overnight gap
    prev_close = df["Close"].shift(1)
    features["price_gap"] = (df["Open"] - prev_close) / prev_close

    #intraday volatility normalized by price
    features["hl_range"] = (df["High"] - df["Low"]) / df["Close"]
    
    #How extreme today's return is vs recent history
    rolling_mean = features["daily_return"].rolling(20).mean()
    rolling_std  = features["daily_return"].rolling(20).std()
    features["return_zscore"] = (features["daily_return"] - rolling_mean) / rolling_std
    
    #drop NaN rows and drop raw OHLCV columns
    feature_cols = ["daily_return", "volume_ratio", "price_gap", "hl_range", "return_zscore"]
    return features[feature_cols].dropna()

#Flags days where the absolute Z-score of returns exceeds the threshold
def flag_return_zscore(features: pd.DataFrame, threshold: float = 3.0) -> pd.Series:
    return features["return_zscore"].abs() > threshold

#Flag days where volume ratio exceeds the threshold
def flag_volume_spike(features: pd.DataFrame, threshold: float = 2.5) -> pd.Series:
    return features["volume_ratio"] > threshold

#Flags days where the overnight gap exceeds 2%
def flag_price_gap(features: pd.DataFrame, threshold: float = 0.02) -> pd.Series:
    return features["price_gap"].abs() > threshold

def isolation_forest_scores(features: pd.DataFrame, contamination: float = 0.05) -> pd.Series:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    model = IsolationForest(contamination = contamination, random_state = 42)
    model.fit(scaled)

    scores = model.decision_function(scaled)
    return pd.Series(scores, index = features.index, name = "iso_score")

def detect_anomalies(
        df: pd.DataFrame,
        contamination: float = 0.5,
        zscore_threshold: float = 3.0,
        volume_threshold: float = 2.5,
        gap_threshold: float = 0.02
    ) -> pd.DataFrame:

    features = build_features(df)
    rule_flags = (
        flag_return_zscore(features, zscore_threshold) |
        flag_volume_spike(features, volume_threshold) |
        flag_price_gap(features, gap_threshold)
    )

    iso_scores = isolation_forest_scores(features, contamination)
    iso_flags = iso_scores < 0

    result = features.copy()
    result["iso_score"] = iso_scores
    result["rule_flagged"] = rule_flags
    result["iso_flagged"] = iso_flags
    result["anomaly"] = rule_flags | iso_flags

    return result