from flask import (
    Flask, render_template, jsonify, abort, request,
    send_file, url_for, session, redirect
)
import pandas as pd
import numpy as np
import os, json, uuid
from datetime import datetime, timedelta

from model_utils import (
    predict_from_frames,
    derive_signals_from_transactions,
    load_model,
)
from i18n import (
    SUPPORTED_LANGS, DEFAULT_LANG, LANG_LABELS, LANG_NAMES, translate,
)


# =====================================================================
# App config
# =====================================================================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-hackathon-secret-change-me")

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_REQUEST_MB = 500    # total request size
MAX_FILES      = 10     # per category (transactions / signals)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_MB * 1024 * 1024


# =====================================================================
# i18n — current language + template helper
# =====================================================================
def get_lang() -> str:
    lang = session.get("lang")
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
    return lang


@app.context_processor
def inject_i18n():
    """Expose `t`, `current_lang`, etc. to every template."""
    lang = get_lang()
    return {
        "t":               lambda key, **kw: translate(lang, key, **kw),
        "current_lang":    lang,
        "supported_langs": SUPPORTED_LANGS,
        "lang_labels":     LANG_LABELS,
        "lang_names":      LANG_NAMES,
    }


@app.route("/set-language/<lang>")
def set_language(lang):
    if lang in SUPPORTED_LANGS:
        session["lang"] = lang
    return redirect(request.referrer or "/")


# =====================================================================
# Data loaders (cached)
# =====================================================================
_cache = {}


def _load(name):
    if name in _cache:
        return _cache[name]
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        return None
    try:
        _cache[name] = pd.read_csv(path)
    except Exception:
        return None
    return _cache[name]


def get_signals():           return _load("data/signals.csv")
def get_transactions():      return _load("data/transactions.csv")
def get_predictions():       return _load("predictions.csv")
def get_oof_predictions():   return _load("oof_predictions.csv")


# =====================================================================
# Metrics for home + dashboard
# =====================================================================
def compute_metrics():
    sig  = get_signals()
    txn  = get_transactions()
    pred = get_oof_predictions()
    if pred is None:
        pred = get_predictions()

    if sig is None or txn is None:
        return None

    m = {
        "n_signals":       int(len(sig)),
        "n_transactions":  int(len(txn)),
        "escalation_rate": float(sig["label"].mean()) if "label" in sig else 0.0,
        "mean_prob":       float(pred["escalation_probability"].mean()) if pred is not None else 0.0,
        "n_escalated":     int(sig["label"].sum()) if "label" in sig else 0,
        "n_dismissed":     int((sig["label"] == 0).sum()) if "label" in sig else 0,
    }

    m["dir_counts"]  = txn["direction"].value_counts().to_dict() if "direction" in txn else {}
    m["type_counts"] = txn["txn_type"].value_counts().head(10).to_dict() if "txn_type" in txn else {}

    if "amount" in txn:
        h, e = np.histogram(np.log1p(txn["amount"].astype(float)), bins=30)
        m["amount_data"] = {"edges": e.tolist(), "counts": h.tolist()}
    else:
        m["amount_data"] = {"edges": [], "counts": []}

    if "signal_id" in txn and "label" in sig:
        tp = (txn.groupby("signal_id").size().rename("n").reset_index()
                 .merge(sig[["signal_id", "label"]], on="signal_id", how="left"))
        m["evd"] = {str(int(k)): float(v)
                    for k, v in tp.groupby("label")["n"].mean().to_dict().items()}
    else:
        m["evd"] = {}

    if pred is not None:
        h, e = np.histogram(pred["escalation_probability"], bins=20, range=(0, 1))
        m["prob_dist"] = {"edges": e.tolist(), "counts": h.tolist()}
    else:
        m["prob_dist"] = {"edges": [], "counts": []}

    return m


def _cleanup_old_uploads(max_age_minutes=60):
    cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)
    for f in os.listdir(UPLOAD_DIR):
        p = os.path.join(UPLOAD_DIR, f)
        try:
            if os.path.isfile(p) and datetime.utcfromtimestamp(os.path.getmtime(p)) < cutoff:
                os.remove(p)
        except OSError:
            pass


def _read_many(files, label):
    """Concatenate several uploaded CSVs into one DataFrame."""
    frames = []
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception as e:
            raise ValueError(
                translate(get_lang(), "err.could_not_read", name=f.filename, err=e)
            )
        df["__source_file"] = f.filename
        frames.append(df)
    if not frames:
        raise ValueError(f"No {label} files could be read.")
    combined = pd.concat(frames, ignore_index=True)
    combined.drop(columns=["__source_file"], inplace=True, errors="ignore")
    return combined


# =====================================================================
# Pages
# =====================================================================
@app.route("/")
def home():
    return render_template("index.html", metrics=compute_metrics())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
def dashboard():
    m = compute_metrics()
    if m is None:
        return render_template("dashboard.html", metrics=None), 200
    return render_template(
        "dashboard.html",
        metrics=m,
        dir_counts=json.dumps(m["dir_counts"]),
        type_counts=json.dumps(m["type_counts"]),
        amount_data=json.dumps(m["amount_data"]),
        prob_dist=json.dumps(m["prob_dist"]),
        evd=json.dumps(m["evd"]),
    )


@app.route("/predictions")
def predictions():
    sig = get_signals()

    # Prefer out-of-fold (honest) predictions, fall back to in-sample
    oof = get_oof_predictions()
    if oof is not None:
        pred = oof.copy()
        pred_source = "out-of-fold (5-fold CV)"
    else:
        pred = get_predictions()
        pred_source = "in-sample (trained on full data)"

    if pred is None:
        return render_template("predictions.html",
                               preds=[], top=[], pred_source=pred_source)

    # Merge ground truth
    if sig is not None and "label" in sig.columns:
        pred = pred.merge(sig[["signal_id", "label"]], on="signal_id", how="left")
    else:
        pred["label"] = None

    # Binary classification at 0.5
    pred["predicted"] = (pred["escalation_probability"] >= 0.5).astype(int)

    accuracy = None
    tp = fp = tn = fn = 0
    if pred["label"].notna().any():
        correct = (pred["predicted"] == pred["label"]).sum()
        accuracy = float(correct) / len(pred)
        tp = int(((pred["predicted"] == 1) & (pred["label"] == 1)).sum())
        fp = int(((pred["predicted"] == 1) & (pred["label"] == 0)).sum())
        tn = int(((pred["predicted"] == 0) & (pred["label"] == 0)).sum())
        fn = int(((pred["predicted"] == 0) & (pred["label"] == 1)).sum())

    pred_sorted = pred.sort_values("escalation_probability", ascending=False)

    def _clean(df):
        records = df.to_dict(orient="records")
        for r in records:
            if r.get("label") is not None and pd.notna(r["label"]):
                r["label"] = int(r["label"])
            else:
                r["label"] = None
            r["correct"] = (
                r["label"] is not None and r["predicted"] == r["label"]
            )
        return records

    return render_template(
        "predictions.html",
        preds=_clean(pred_sorted),
        top=_clean(pred_sorted.head(20)),
        n_total=len(pred),
        n_high=int((pred["escalation_probability"] >= 0.7).sum()),
        n_mid=int(((pred["escalation_probability"] >= 0.3) &
                   (pred["escalation_probability"] < 0.7)).sum()),
        n_low=int((pred["escalation_probability"] < 0.3).sum()),
        accuracy=accuracy,
        tp=tp, fp=fp, tn=tn, fn=fn,
        pred_source=pred_source,
    )


# =====================================================================
# Predict — upload + score
# =====================================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    def _model_info():
        info = {"max_files": MAX_FILES, "max_mb": MAX_REQUEST_MB}
        try:
            art = load_model()
            info["n_features"] = len(art["features"])
        except FileNotFoundError as e:
            info["error"] = str(e)
        return info

    def _back(error=None, success=None):
        return render_template(
            "predict.html",
            model_info=_model_info(),
            error=error,
            success=success,
        )

    if request.method == "GET":
        return _back()

    _cleanup_old_uploads()

    txn_files = [f for f in request.files.getlist("transactions") if f and f.filename]
    sig_files = [f for f in request.files.getlist("signals")      if f and f.filename]

    lang = get_lang()

    if not txn_files:
        return _back(error=translate(lang, "err.no_txn"))
    if len(txn_files) > MAX_FILES:
        return _back(error=translate(lang, "err.too_many_files", n=MAX_FILES))
    if len(sig_files) > MAX_FILES:
        return _back(error=translate(lang, "err.too_many_files", n=MAX_FILES))

    # Transactions (required)
    try:
        txns = _read_many(txn_files, "transactions")
    except ValueError as e:
        return _back(error=str(e))
    if len(txns) == 0:
        return _back(error=translate(lang, "err.empty_txn"))

    # Signals (optional)
    if sig_files:
        try:
            signals = _read_many(sig_files, "signals")
        except ValueError as e:
            return _back(error=str(e))
        if len(signals) == 0:
            return _back(error=translate(lang, "err.empty_sig"))
    else:
        try:
            signals = derive_signals_from_transactions(txns)
        except Exception as e:
            return _back(error=translate(lang, "err.could_not_derive", err=e))

    # Inference
    try:
        preds = predict_from_frames(signals, txns)
    except Exception as e:
        return _back(error=translate(lang, "err.pred_failed", err=e))

    # Save for download
    token = uuid.uuid4().hex[:12]
    out_path = os.path.join(UPLOAD_DIR, f"predictions_{token}.csv")
    preds.to_csv(out_path, index=False)

    # Summary
    n_total = len(preds)
    n_high  = int((preds["escalation_probability"] >= 0.7).sum())
    n_mid   = int(((preds["escalation_probability"] >= 0.3) &
                   (preds["escalation_probability"] < 0.7)).sum())
    n_low   = int((preds["escalation_probability"] < 0.3).sum())

    # If the user uploaded signals with labels, compute accuracy live
    accuracy = None
    tp = fp = tn = fn = 0
    if "label" in signals.columns and signals["label"].notna().any():
        merged = preds.merge(
            signals[["signal_id", "label"]], on="signal_id", how="left"
        )
        merged["predicted"] = (merged["escalation_probability"] >= 0.5).astype(int)
        valid = merged["label"].notna()
        if valid.any():
            correct = (merged.loc[valid, "predicted"] == merged.loc[valid, "label"]).sum()
            accuracy = float(correct) / int(valid.sum())
            tp = int(((merged["predicted"] == 1) & (merged["label"] == 1)).sum())
            fp = int(((merged["predicted"] == 1) & (merged["label"] == 0)).sum())
            tn = int(((merged["predicted"] == 0) & (merged["label"] == 0)).sum())
            fn = int(((merged["predicted"] == 0) & (merged["label"] == 1)).sum())

    return _back(success={
        "token":     token,
        "n_total":   n_total,
        "n_high":    n_high,
        "n_mid":     n_mid,
        "n_low":     n_low,
        "mean_prob": float(preds["escalation_probability"].mean()),
        "max_prob":  float(preds["escalation_probability"].max()),
        "min_prob":  float(preds["escalation_probability"].min()),
        "top":       preds.head(25).to_dict(orient="records"),
        "accuracy":  accuracy,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "has_labels": accuracy is not None,
    })


@app.route("/download/<token>")
def download(token):
    if not token.replace("_", "").isalnum():
        abort(400)
    path = os.path.join(UPLOAD_DIR, f"predictions_{token}.csv")
    if not os.path.exists(path):
        abort(404)
    return send_file(
        path,
        as_attachment=True,
        download_name=f"predictions_{token}.csv",
        mimetype="text/csv",
    )


# =====================================================================
# JSON API
# =====================================================================
@app.route("/api/metrics")
def api_metrics():
    m = compute_metrics()
    if m is None:
        abort(503)
    return jsonify(m)


@app.route("/api/predictions")
def api_predictions():
    pred = get_oof_predictions()
    if pred is None:
        pred = get_predictions()
    if pred is None:
        abort(503)
    return jsonify(pred.head(100).to_dict(orient="records"))


# =====================================================================
# Errors
# =====================================================================
@app.errorhandler(413)
def too_large(_e):
    return render_template(
        "predict.html",
        model_info={
            "max_files": MAX_FILES,
            "max_mb": MAX_REQUEST_MB,
        },
        error=translate(
            get_lang(),
            "err.too_many_files",
            n=f"{MAX_REQUEST_MB} MB",
        ),
        success=None,
    ), 413


# =====================================================================
# Dev server
# =====================================================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)