"""
Generate realistic (NOISY) dummy data for the Signal Escalation hackathon.

Key changes vs. the "clean" generator:
  - Escalated and dismissed distributions OVERLAP heavily
  - 20% of labels are FLIPPED (noise) → no perfect separation
  - Amount distributions overlap → not trivially separable
  - Temporal windows are blurred across classes

Expected OOF ROC-AUC: 0.78 – 0.88 (realistic)
Expected prediction spread: 0.02 → 0.97, not 0.0001 / 0.9998
"""

import os, random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RANDOM_STATE = 42
random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Config — tuned for realistic overlap
# ------------------------------------------------------------------
N_SIGNALS       = 1200
ESCALATION_RATE = 0.30
LABEL_NOISE     = 0.15        # 15% of labels are randomly flipped

START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)

SIGNAL_TYPES = ["velocity", "geo_anomaly", "amount_spike", "device_change",
                "structuring", "unusual_hours", "counterparty_risk"]
CHANNELS     = ["mobile", "web", "branch", "api", "atm"]
TXN_TYPES    = ["transfer", "payment", "withdrawal", "deposit", "card_purchase",
                "wire", "fx_exchange", "refund", "atm_withdrawal", "bill_pay"]
CURRENCIES   = ["USD", "EUR", "GBP", "JPY", "CHF"]
HOME_COUNTRY = "US"
FOREIGN_COUNTRIES = ["RU", "CN", "NG", "BR", "KY", "PA", "AE", "TR", "IN", "UA"]

print("Generating signals...")

signals = []
for i in range(N_SIGNALS):
    sid = f"SIG-{i+1:05d}"
    # True latent class
    latent = 1 if random.random() < ESCALATION_RATE else 0
    # Add label noise: 15% of signals get their label flipped
    label = latent
    if random.random() < LABEL_NOISE:
        label = 1 - latent

    stime = START_DATE + timedelta(
        seconds=random.randint(0, int((END_DATE - START_DATE).total_seconds()))
    )
    signals.append({
        "signal_id":   sid,
        "signal_time": stime,
        "label":       label,
        "signal_type": random.choice(SIGNAL_TYPES),
        "channel":     random.choice(CHANNELS),
        "_latent":     latent,     # for txn generation only (dropped later)
    })

signals_df = pd.DataFrame(signals)
print(f"  → {len(signals_df)} signals, "
      f"escalation rate = {signals_df.label.mean():.2%} "
      f"(latent = {signals_df._latent.mean():.2%})")

# ------------------------------------------------------------------
# Transactions — driven by LATENT class, not label
# ------------------------------------------------------------------
print("Generating transactions...")

transactions = []
txn_counter = 0

for _, sig in signals_df.iterrows():
    sid      = sig["signal_id"]
    stime    = sig["signal_time"]
    is_escal = sig["_latent"] == 1

    # --- Number of txns: heavily overlapping ---
    if is_escal:
        n_txns = max(1, min(int(np.random.gamma(shape=2.5, scale=3.5)) + 4, 60))
    else:
        n_txns = max(1, min(int(np.random.gamma(shape=2.0, scale=2.5)) + 3, 60))

    # --- Time span ---
    if is_escal:
        span_hours = np.random.uniform(48, 24 * 45)
    else:
        span_hours = np.random.uniform(48, 24 * 60)

    for k in range(n_txns):
        txn_counter += 1

        # ~40% of escalated have a burst in the last 24h (not 100%)
        if is_escal and random.random() < 0.40 and k >= n_txns - 3:
            offset_hours = np.random.uniform(0, 24)
        else:
            offset_hours = np.random.uniform(0, span_hours)

        ttime = stime - timedelta(hours=float(offset_hours))

        # --- Amount: overlapping lognormals ---
        # escalated median ≈ $2k, dismissed median ≈ $900 — not 5× apart
        if is_escal:
            amount = float(np.random.lognormal(mean=7.6, sigma=1.3))
        else:
            amount = float(np.random.lognormal(mean=6.8, sigma=1.2))
        amount = round(amount, 2)

        # --- Direction ---
        if is_escal:
            direction = "in" if random.random() < 0.58 else "out"
        else:
            direction = "in" if random.random() < 0.50 else "out"

        # --- Country: escalated slightly more international ---
        intl_p = 0.28 if is_escal else 0.18
        country = (random.choice(FOREIGN_COUNTRIES)
                   if random.random() < intl_p else HOME_COUNTRY)

        # --- Type ---
        if is_escal:
            txn_type = random.choices(TXN_TYPES,
                weights=[18, 15, 10, 10, 12, 12, 8, 4, 6, 5], k=1)[0]
        else:
            txn_type = random.choices(TXN_TYPES,
                weights=[10, 20, 10, 12, 18, 6, 3, 5, 9, 7], k=1)[0]

        currency = "USD" if country == HOME_COUNTRY else random.choice(CURRENCIES)

        transactions.append({
            "txn_id":    f"TXN-{txn_counter:08d}",
            "signal_id": sid,
            "txn_time":  ttime,
            "amount":    amount,
            "direction": direction,
            "txn_type":  txn_type,
            "country":   country,
            "currency":  currency,
        })

txns_df = pd.DataFrame(transactions)
print(f"  → {len(txns_df)} transactions")

# ------------------------------------------------------------------
# Shuffle + save (drop the private _latent column)
# ------------------------------------------------------------------
signals_df = signals_df.drop(columns=["_latent"])
signals_df = signals_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
txns_df    = txns_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

signals_df.to_csv(os.path.join(OUT_DIR, "signals.csv"), index=False)
txns_df.to_csv(os.path.join(OUT_DIR, "transactions.csv"), index=False)

print(f"\n✅ Wrote {OUT_DIR}/signals.csv      ({len(signals_df)} rows)")
print(f"✅ Wrote {OUT_DIR}/transactions.csv ({len(txns_df)} rows)")

# ------------------------------------------------------------------
# Quick summary
# ------------------------------------------------------------------
merged = txns_df.merge(signals_df[["signal_id", "label"]], on="signal_id")
summary = merged.groupby("label").agg(
    n_txns      = ("txn_id", "count"),
    mean_amount = ("amount", "mean"),
    median_amt  = ("amount", "median"),
    intl_share  = ("country", lambda s: (s != HOME_COUNTRY).mean()),
    in_share    = ("direction", lambda s: (s == "in").mean()),
).round(3)
print("\n--- Class-conditional summary ---")
print(summary)
print("\nClasses OVERLAP — the model must work for its AUC.")