"""Model inference utilities — shared between the notebook and the web app."""
import os
import numpy as np
import pandas as pd
import joblib

_HERE = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(os.path.dirname(_HERE), "models", "lgbm_model.pkl")

_MODEL_CACHE = None


def load_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is not None:
        return _MODEL_CACHE
    if not os.path.exists(_MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {_MODEL_PATH}. "
            f"Run the notebook first to generate models/lgbm_model.pkl."
        )
    _MODEL_CACHE = joblib.load(_MODEL_PATH)
    return _MODEL_CACHE


def _normalize_signals(s: pd.DataFrame) -> pd.DataFrame:
    sig_renames = {
        "id": "signal_id", "signalId": "signal_id", "signal": "signal_id",
        "timestamp": "signal_time", "time": "signal_time", "created_at": "signal_time",
        "datetime": "signal_time", "date": "signal_time",
        "is_escalated": "label", "escalated": "label", "target": "label",
        "y": "label", "class": "label", "outcome": "label",
        "type": "signal_type", "signaltype": "signal_type",
    }
    s = s.rename(columns={k: v for k, v in sig_renames.items() if k in s.columns})

    if "signal_id" not in s.columns:
        raise ValueError("signals data must contain a 'signal_id' column.")
    if "label" not in s.columns:
        s["label"] = 0
    if "signal_time" not in s.columns:
        s["signal_time"] = pd.Timestamp.utcnow()
    s["signal_time"] = pd.to_datetime(s["signal_time"], errors="coerce")
    s["signal_time"] = s["signal_time"].fillna(pd.Timestamp.utcnow())
    return s


def _normalize_txns(t: pd.DataFrame) -> pd.DataFrame:
    txn_renames = {
        "id": "txn_id", "transaction_id": "txn_id", "transactionId": "txn_id",
        "transaction": "txn_id",
        "timestamp": "txn_time", "time": "txn_time", "created_at": "txn_time",
        "datetime": "txn_time", "date": "txn_time",
        "value": "amount", "sum": "amount", "amount_usd": "amount",
        "type": "txn_type", "transaction_type": "txn_type",
        "flow": "direction", "kind": "direction", "io": "direction",
        "country_code": "country", "geo": "country",
    }
    t = t.rename(columns={k: v for k, v in txn_renames.items() if k in t.columns})

    if "signal_id" not in t.columns:
        raise ValueError("transactions data must contain a 'signal_id' column.")

    # Required with defaults
    if "txn_id" not in t.columns:
        t["txn_id"] = range(len(t))
    if "amount" not in t.columns:
        t["amount"] = 0.0
    if "country" not in t.columns:
        t["country"] = "HOME"
    if "direction" not in t.columns:
        t["direction"] = "in"
    if "txn_type" not in t.columns:
        t["txn_type"] = "unknown"
    if "currency" not in t.columns:
        t["currency"] = "USD"

    # txn_time is the tricky one — flag if it's missing
    t.attrs["_had_txn_time"] = "txn_time" in t.columns
    if t.attrs["_had_txn_time"]:
        t["txn_time"] = pd.to_datetime(t["txn_time"], errors="coerce")

    return t


def build_features(signals: pd.DataFrame, txns: pd.DataFrame) -> pd.DataFrame:
    """Turn raw signals + transactions into one feature row per signal_id."""
    s = _normalize_signals(signals.copy())
    t = _normalize_txns(txns.copy())
    had_txn_time = t.attrs.get("_had_txn_time", False)

    # Attach signal_time to each txn
    t = t.merge(s[["signal_id", "signal_time"]], on="signal_id", how="left")

    # Fallback: no txn_time → treat every txn as happening at signal time
    if not had_txn_time:
        t["txn_time"] = t["signal_time"]
    else:
        t["txn_time"] = t["txn_time"].fillna(t["signal_time"])

    t["dt_hours"] = (t["signal_time"] - t["txn_time"]).dt.total_seconds() / 3600
    # Guard against negative dt (txn after signal)
    t["dt_hours"] = t["dt_hours"].clip(lower=0)

    # ---- Base aggregations ----
    g = t.groupby("signal_id")
    feats = g.agg(
        n_txns         = ("txn_id",  "count"),
        total_amount   = ("amount",  "sum"),
        mean_amount    = ("amount",  "mean"),
        median_amount  = ("amount",  "median"),
        std_amount     = ("amount",  "std"),
        max_amount     = ("amount",  "max"),
        min_amount     = ("amount",  "min"),
        sum_log_amount = ("amount",  lambda x: np.log1p(x).sum()),
        n_unique_types = ("txn_type","nunique"),
        n_unique_ctry  = ("country", "nunique"),
    ).reset_index()

    # ---- Direction ----
    t["is_in"] = (t["direction"].astype(str).str.lower() == "in").astype(int)
    dir_feats = g["is_in"].agg(["mean", "sum"]).rename(
        columns={"mean": "in_ratio", "sum": "n_in"}).reset_index()
    feats = feats.merge(dir_feats, on="signal_id", how="left")
    feats["n_out"]     = feats["n_txns"] - feats["n_in"]
    feats["out_ratio"] = 1 - feats["in_ratio"]

    # ---- International ----
    home = t["country"].mode().iloc[0] if len(t) else "HOME"
    t["is_intl"] = (t["country"] != home).astype(int)
    intl = g["is_intl"].agg(["mean", "sum"]).rename(
        columns={"mean": "intl_ratio", "sum": "n_intl"}).reset_index()
    feats = feats.merge(intl, on="signal_id", how="left")

    # ---- Top-10 txn types ----
    top_types = t["txn_type"].value_counts().head(10).index.tolist()
    for tt in top_types:
        col = f"type_{str(tt).replace(' ', '_')}_ratio"
        r = (t.assign(_hits=(t.txn_type == tt).astype(int))
               .groupby("signal_id")["_hits"].mean()
               .rename(col).reset_index())
        feats = feats.merge(r, on="signal_id", how="left")

    # ---- Temporal windows ----
    for name, h in {"1h": 1, "6h": 6, "24h": 24, "7d": 168}.items():
        sub = t[t["dt_hours"].between(0, h)]
        cnt = sub.groupby("signal_id").size().rename(f"n_last_{name}").reset_index()
        amt = sub.groupby("signal_id")["amount"].sum().rename(f"amt_last_{name}").reset_index()
        feats = feats.merge(cnt, on="signal_id", how="left") \
                     .merge(amt, on="signal_id", how="left")

    # ---- Time deltas ----
    last_dt  = t.sort_values("dt_hours").groupby("signal_id")["dt_hours"].min() \
                .rename("hours_since_last_txn").reset_index()
    first_dt = t.sort_values("dt_hours").groupby("signal_id")["dt_hours"].max() \
                .rename("hours_since_first_txn").reset_index()
    feats = feats.merge(last_dt,  on="signal_id", how="left") \
                 .merge(first_dt, on="signal_id", how="left")

    # ---- Velocity / ratios ----
    feats["txn_velocity_24h"] = feats["n_last_24h"] / feats["n_txns"].clip(lower=1)
    feats["amt_velocity_24h"] = feats["amt_last_24h"] / feats["total_amount"].clip(lower=1)
    feats["log_total_amount"] = np.log1p(feats["total_amount"])
    feats["amt_per_txn"]      = feats["total_amount"] / feats["n_txns"].clip(lower=1)
    feats["span_hours"]       = feats["hours_since_first_txn"] - feats["hours_since_last_txn"]

    fill0 = [c for c in feats.columns if c != "signal_id"]
    feats[fill0] = feats[fill0].fillna(0)

    # ---- Signal-level metadata ----
    meta_cols = [c for c in ["signal_id", "signal_type", "channel"] if c in s.columns]
    out = s[meta_cols].merge(feats, on="signal_id", how="left")
    out[fill0] = out[fill0].fillna(0)

    cat_cols = [c for c in ["signal_type", "channel"] if c in out.columns]
    if cat_cols:
        out = pd.get_dummies(out, columns=cat_cols, dummy_na=False)

    return out


def predict_from_frames(signals: pd.DataFrame, txns: pd.DataFrame) -> pd.DataFrame:
    art = load_model()
    feat_df = build_features(signals, txns)
    for c in art["features"]:
        if c not in feat_df.columns:
            feat_df[c] = 0.0
    Xnew = feat_df[art["features"]].astype(float).values
    proba = art["model"].predict_proba(Xnew)[:, 1]
    return pd.DataFrame({
        "signal_id": feat_df["signal_id"],
        "escalation_probability": proba,
    }).sort_values("escalation_probability", ascending=False).reset_index(drop=True)


def derive_signals_from_transactions(txns: pd.DataFrame) -> pd.DataFrame:
    if "signal_id" not in txns.columns:
        raise ValueError("transactions data must contain a 'signal_id' column.")
    sig_ids = txns["signal_id"].dropna().unique().tolist()

    if "txn_time" in txns.columns:
        t = txns.copy()
        t["txn_time"] = pd.to_datetime(t["txn_time"], errors="coerce")
        times = t.groupby("signal_id")["txn_time"].max().reindex(sig_ids).values
    else:
        times = [pd.Timestamp.utcnow()] * len(sig_ids)

    return pd.DataFrame({"signal_id": sig_ids, "signal_time": times, "label": 0})