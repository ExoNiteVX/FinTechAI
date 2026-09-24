"""Simple i18n — English / Russian / Uzbek (Latin).

Add a new string by:
1. Picking a unique key like "home.title_1"
2. Adding it to all three language dicts below
3. Using {{ t('home.title_1') }} in templates
"""

SUPPORTED_LANGS = ["en", "ru", "uz"]
DEFAULT_LANG    = "en"
LANG_LABELS     = {"en": "EN", "ru": "RU", "uz": "UZ"}
LANG_NAMES      = {"en": "English", "ru": "Русский", "uz": "O'zbekcha"}

TRANSLATIONS = {
    # =====================================================================
    # ENGLISH
    # =====================================================================
    "en": {
        # Nav
        "nav.home":         "Home",
        "nav.about":        "About",
        "nav.dashboard":    "Dashboard",
        "nav.predictions":  "Predictions",
        "nav.predict":      "Try it",
        "nav.footer":       "EscalationLens · Built for the Hackathon · LightGBM + Flask · ROC-AUC evaluated",

        # Hero (index)
        "home.badge":           "Model live · ROC-AUC optimized",
        "home.title_1":         "Predict which financial signals",
        "home.title_2":         "deserve investigation.",
        "home.subtitle":        "EscalationLens turns raw transaction histories into calibrated escalation probabilities — so your team spends time on the signals that matter.",
        "home.cta_dashboard":   "📊 View Dashboard",
        "home.cta_predictions": "🎯 See Predictions",
        "home.cta_about":       "📖 How it works",

        # Home — features
        "home.feat_eyebrow": "Capabilities",
        "home.feat_title":   "Everything from raw transactions to ranked signals",
        "home.feat_sub":     "An end-to-end pipeline: feature engineering, gradient-boosted trees, and a modern interface to act on the scores.",
        "home.f1_t": "Automated Feature Engineering",
        "home.f1_d": "Transaction counts, amounts, direction mix, international share, temporal windows (1h → 7d) — all computed per signal.",
        "home.f2_t": "Gradient-Boosted Trees",
        "home.f2_d": "LightGBM classifier with stratified 5-fold cross-validation and early stopping. Ranked by ROC-AUC, not just accuracy.",
        "home.f3_t": "Calibrated Probabilities",
        "home.f3_d": "Each signal receives a score in [0, 1] — ready for triage thresholds or downstream human review queues.",
        "home.f4_t": "Explainable by Design",
        "home.f4_d": "Feature-importance rankings show exactly which signal patterns drove the model's decisions.",
        "home.f5_t": "REST API",
        "home.f5_d": "Feed scores into any system via /api/predictions and /api/metrics.",
        "home.f6_t": "Fast & Self-contained",
        "home.f6_d": "One Flask app, one trained model artifact, zero external dependencies at inference time.",
        "home.cta_title": "Ready to explore the data?",
        "home.cta_desc":  "Jump into the interactive dashboard to see how escalated signals differ from dismissed ones.",
        "home.cta_btn":   "Open Dashboard →",

        # KPI labels (shared across pages)
        "kpi.signals":            "Signals",
        "kpi.transactions":       "Transactions",
        "kpi.escalation_rate":    "Escalation rate",
        "kpi.mean_prob":          "Mean predicted prob.",
        "kpi.signals_analysed":   "Signals analysed",
        "kpi.historic_signals":   "historic labeled signals",
        "kpi.across_signals":     "across all signals",
        "kpi.of_signals":         "{a} of {b}",
        "kpi.across_all":         "across all signals",
        "kpi.signals_scored":     "Signals scored",
        "kpi.high_risk":          "High risk (≥ 0.7)",
        "kpi.medium_risk":        "Medium (0.3 – 0.7)",
        "kpi.low_risk":           "Low risk (< 0.3)",
        "kpi.total_scored":       "Total scored",
        "kpi.mean_prob_short":    "Mean probability",
        "kpi.max_short":          "max {p}",

        # Pills
        "band.escalate": "escalate",
        "band.review":   "review",
        "band.dismiss":  "dismiss",

        # Predict page
        "predict.eyebrow":      "Try the model",
        "predict.title":        "Upload your data",
        "predict.subtitle":     "Upload one or more transactions.csv files (required) and optionally signals.csv files. We'll concatenate them and score every signal.",
        "predict.required":     "required",
        "predict.optional":     "optional",
        "predict.dz_txn_title":"transactions.csv",
        "predict.dz_sig_title":"signals.csv",
        "predict.dz_txn_hint": "Click or drag up to {n} CSV files",
        "predict.dz_sig_hint": "If omitted, we'll derive one signal per signal_id",
        "predict.run":         "🚀 Run prediction",
        "predict.running":     "⏳ Running model…",
        "predict.note":        "Up to {n} files · {mb} MB total · Model has {f} features",
        "predict.expected_title":"Expected columns",
        "predict.expected_txn":"transactions.csv (required):",
        "predict.expected_sig":"signals.csv (optional):",
        "predict.expected_foot":"Missing columns are auto-filled with defaults. Common aliases (timestamp, transaction_id, date, type, …) are auto-recognised.",
        "predict.success":     "✅ Prediction complete",
        "predict.download":    "⬇️ Download predictions.csv",
        "predict.top_table":   "Top 25 highest-risk signals",
        "predict.showing":     "Showing 25 of {n} — download the CSV for the full list.",
        "predict.model_unavail":"Model unavailable.",
        "predict.error_prefix":"Error:",

        # Table headers
        "table.rank":        "#",
        "table.signal_id":   "Signal ID",
        "table.probability": "Probability",
        "table.band":        "Band",

        # Predictions page
        "pred.eyebrow":  "Model output",
        "pred.title":    "Ranked Escalation Probabilities",
        "pred.subtitle": "Every signal scored by the trained LightGBM model, sorted from highest to lowest risk.",
        "pred.top20":    "Top 20 highest-risk signals",
        "pred.all":      "All signals ({n} total)",
        "pred.empty_t":  "No predictions found",
        "pred.empty_d":  "Run the notebook to generate predictions.csv.",
        "pred.api_t":    "Machine-readable output",
        "pred.api_d":    "Fetch the same data as JSON from /api/predictions.",

                # Predictions page — extra keys
        "table.ground_truth": "Ground truth",
        "table.predicted":    "Predicted",
        "table.match":        "Match",

        "gt.escalated":  "1 · escalated",
        "gt.dismissed":  "0 · dismissed",

        "pred.acc_title":   "Model accuracy on this dataset",
        "pred.acc_line":    "At threshold 0.5, {p}% of signals are classified correctly",
        "pred.acc_correct": "✅ Correct",
        "pred.acc_tp":      "True Positives",
        "pred.acc_tp_sub":  "escalated & correctly flagged",
        "pred.acc_fp":      "False Positives",
        "pred.acc_fp_sub":  "dismissed but flagged",
        "pred.acc_fn":      "False Negatives",
        "pred.acc_fn_sub":  "escalated but missed",

        "pred.chart_hist":   "Predicted probability distribution",
        "pred.chart_conf":   "Confusion matrix @ 0.5",
        "pred.cm_tp":        "True Positive",
        "pred.cm_fp":        "False Positive",
        "pred.cm_tn":        "True Negative",
        "pred.cm_fn":        "False Negative",
        "pred.cm_no_labels": "No ground-truth labels available",


        # Dashboard
        "dash.eyebrow":  "Live EDA",
        "dash.title":    "Exploratory Data Analysis",
        "dash.subtitle": "Interactive views of the transaction data behind the model.",
        "dash.empty_t":  "No data found",
        "dash.empty_d":  "Make sure data/signals.csv and data/transactions.csv exist.",
        "dash.p_dir":    "Incoming vs Outgoing",
        "dash.p_types":  "Top transaction types",
        "dash.p_amt":    "Amount distribution (log1p)",
        "dash.p_evd":    "Avg txns / signal by class",
        "dash.p_prob":   "Predicted probability distribution",

        # About
        "about.eyebrow":  "About the project",
        "about.title":    "How EscalationLens works",
        "about.subtitle": "From a stream of transactions to a ranked list of signals worth investigating.",
        "about.p1": "Load",  "about.p1d": "Ingest signals.csv and transactions.csv.",
        "about.p2": "Explore","about.p2d": "Compare escalated vs. dismissed: counts, amounts, direction, country, timing.",
        "about.p3": "Engineer","about.p3d": "~50 features per signal: aggregations, ratios, temporal windows, one-hot types.",
        "about.p4": "Train",  "about.p4d": "LightGBM with 5-fold stratified CV and early stopping on AUC.",
        "about.p5": "Score",  "about.p5d": "Emit a probability in [0, 1] per signal — ranked for triage.",

        # Errors
        "err.too_many_files":  "Too many files (max {n}).",
        "err.no_txn":          "Please upload at least one transactions CSV.",
        "err.empty_txn":       "No rows found in transactions data.",
        "err.empty_sig":       "No rows found in signals data.",
        "err.could_not_read":  "Could not read {name}: {err}",
        "err.could_not_derive":"Could not derive signals: {err}",
        "err.pred_failed":     "Prediction failed: {err}",
    },

    # =====================================================================
    # RUSSIAN
    # =====================================================================
    "ru": {
        "nav.home":         "Главная",
        "nav.about":        "О проекте",
        "nav.dashboard":    "Дашборд",
        "nav.predictions":  "Прогнозы",
        "nav.predict":      "Попробовать",
        "nav.footer":       "EscalationLens · Проект для хакатона · LightGBM + Flask · Оценка по ROC-AUC",

        "home.badge":           "Модель активна · ROC-AUC оптимизирован",
        "home.title_1":         "Прогнозируйте, какие финансовые сигналы",
        "home.title_2":         "заслуживают расследования.",
        "home.subtitle":        "EscalationLens превращает историю транзакций в калиброванные вероятности эскалации — чтобы ваша команда тратила время на сигналы, которые действительно важны.",
        "home.cta_dashboard":   "📊 Открыть дашборд",
        "home.cta_predictions": "🎯 Смотреть прогнозы",
        "home.cta_about":       "📖 Как это работает",

        "home.feat_eyebrow": "Возможности",
        "home.feat_title":   "От сырых транзакций до ранжированных сигналов",
        "home.feat_sub":     "Сквозной пайплайн: инженерия признаков, градиентный бустинг и современный интерфейс для работы с результатами.",
        "home.f1_t": "Автоматическая инженерия признаков",
        "home.f1_d": "Количество транзакций, суммы, направление, доля международных, временные окна (1ч → 7д) — всё рассчитывается по каждому сигналу.",
        "home.f2_t": "Градиентный бустинг",
        "home.f2_d": "Классификатор LightGBM со стратифицированной 5-фолдовой кросс-валидацией и ранней остановкой. Оценка по ROC-AUC.",
        "home.f3_t": "Калиброванные вероятности",
        "home.f3_d": "Каждый сигнал получает оценку в [0, 1] — готово для порогов или очереди ручной проверки.",
        "home.f4_t": "Объяснимость",
        "home.f4_d": "Рейтинг важности признаков показывает, какие паттерны повлияли на решение модели.",
        "home.f5_t": "REST API",
        "home.f5_d": "Передавайте оценки в любую систему через /api/predictions и /api/metrics.",
        "home.f6_t": "Быстро и автономно",
        "home.f6_d": "Одно Flask-приложение, один артефакт модели, без внешних зависимостей при инференсе.",
        "home.cta_title": "Готовы изучить данные?",
        "home.cta_desc":  "Откройте интерактивный дашборд, чтобы увидеть, чем эскалированные сигналы отличаются от отклонённых.",
        "home.cta_btn":   "Открыть дашборд →",

        "kpi.signals":            "Сигналы",
        "kpi.transactions":       "Транзакции",
        "kpi.escalation_rate":    "Доля эскалаций",
        "kpi.mean_prob":          "Средняя вероятность",
        "kpi.signals_analysed":   "Проанализировано сигналов",
        "kpi.historic_signals":   "исторических сигналов с меткой",
        "kpi.across_signals":     "по всем сигналам",
        "kpi.of_signals":         "{a} из {b}",
        "kpi.across_all":         "по всем сигналам",
        "kpi.signals_scored":     "Оценено сигналов",
        "kpi.high_risk":          "Высокий риск (≥ 0.7)",
        "kpi.medium_risk":        "Средний (0.3 – 0.7)",
        "kpi.low_risk":           "Низкий риск (< 0.3)",
        "kpi.total_scored":       "Всего оценено",
        "kpi.mean_prob_short":    "Средняя вероятность",
        "kpi.max_short":          "макс {p}",

        "band.escalate": "эскалация",
        "band.review":   "проверить",
        "band.dismiss":  "отклонить",

        "predict.eyebrow":      "Попробуйте модель",
        "predict.title":        "Загрузите свои данные",
        "predict.subtitle":     "Загрузите один или несколько файлов transactions.csv (обязательно) и, при наличии, signals.csv. Они будут объединены, и все сигналы получат оценку.",
        "predict.required":     "обязательно",
        "predict.optional":     "опционально",
        "predict.dz_txn_title":"transactions.csv",
        "predict.dz_sig_title":"signals.csv",
        "predict.dz_txn_hint": "Нажмите или перетащите до {n} CSV-файлов",
        "predict.dz_sig_hint": "Если пропустить, создадим по одному сигналу на signal_id",
        "predict.run":         "🚀 Запустить прогноз",
        "predict.running":     "⏳ Модель работает…",
        "predict.note":        "До {n} файлов · {mb} МБ всего · У модели {f} признаков",
        "predict.expected_title":"Ожидаемые столбцы",
        "predict.expected_txn":"transactions.csv (обязательно):",
        "predict.expected_sig":"signals.csv (опционально):",
        "predict.expected_foot":"Отсутствующие столбцы заполняются значениями по умолчанию. Распознаются псевдонимы (timestamp, transaction_id, date, type, …).",
        "predict.success":     "✅ Прогноз готов",
        "predict.download":    "⬇️ Скачать predictions.csv",
        "predict.top_table":   "Топ 25 самых рискованных сигналов",
        "predict.showing":     "Показано 25 из {n} — скачайте CSV для полного списка.",
        "predict.model_unavail":"Модель недоступна.",
        "predict.error_prefix":"Ошибка:",

        "table.ground_truth": "Истина",
        "table.predicted":    "Прогноз",
        "table.match":        "Совпадение",

        "gt.escalated":  "1 · эскалация",
        "gt.dismissed":  "0 · отклонён",

        "pred.acc_title":   "Точность модели на этих данных",
        "pred.acc_line":    "При пороге 0.5 правильно классифицировано {p}% сигналов",
        "pred.acc_correct": "✅ Верно",
        "pred.acc_tp":      "Истинно положительные",
        "pred.acc_tp_sub":  "эскалация — верно отмечено",
        "pred.acc_fp":      "Ложноположительные",
        "pred.acc_fp_sub":  "отклонён — но отмечен",
        "pred.acc_fn":      "Ложноотрицательные",
        "pred.acc_fn_sub":  "эскалация — но пропущено",

        "pred.chart_hist":   "Распределение предсказанных вероятностей",
        "pred.chart_conf":   "Матрица ошибок при пороге 0.5",
        "pred.cm_tp":        "Истинно положительные",
        "pred.cm_fp":        "Ложноположительные",
        "pred.cm_tn":        "Истинно отрицательные",
        "pred.cm_fn":        "Ложноотрицательные",
        "pred.cm_no_labels": "Истинные метки недоступны",

        "table.rank":        "#",
        "table.signal_id":   "ID сигнала",
        "table.probability": "Вероятность",
        "table.band":        "Категория",

        "pred.eyebrow":  "Результат модели",
        "pred.title":    "Ранжированные вероятности эскалации",
        "pred.subtitle": "Все сигналы, оценённые обученной моделью LightGBM, отсортированы по убыванию риска.",
        "pred.top20":    "Топ 20 самых рискованных сигналов",
        "pred.all":      "Все сигналы (всего {n})",
        "pred.empty_t":  "Прогнозы не найдены",
        "pred.empty_d":  "Запустите ноутбук, чтобы сгенерировать predictions.csv.",
        "pred.api_t":    "Машиночитаемый вывод",
        "pred.api_d":    "Получить те же данные в JSON по адресу /api/predictions.",

        "dash.eyebrow":  "EDA в реальном времени",
        "dash.title":    "Разведочный анализ данных",
        "dash.subtitle": "Интерактивные графики транзакционных данных за моделью.",
        "dash.empty_t":  "Данные не найдены",
        "dash.empty_d":  "Убедитесь, что существуют data/signals.csv и data/transactions.csv.",
        "dash.p_dir":    "Входящие vs Исходящие",
        "dash.p_types":  "Топ типов транзакций",
        "dash.p_amt":    "Распределение сумм (log1p)",
        "dash.p_evd":    "Среднее число транзакций по классу",
        "dash.p_prob":   "Распределение предсказанных вероятностей",

        "about.eyebrow":  "О проекте",
        "about.title":    "Как работает EscalationLens",
        "about.subtitle": "От потока транзакций к ранжированному списку сигналов для расследования.",
        "about.p1": "Загрузка", "about.p1d": "Читаем signals.csv и transactions.csv.",
        "about.p2": "Анализ",   "about.p2d": "Сравниваем эскалированные и отклонённые: количество, суммы, направление, страна, время.",
        "about.p3": "Признаки", "about.p3d": "~50 признаков на сигнал: агрегаты, доли, временные окна, one-hot типы.",
        "about.p4": "Обучение", "about.p4d": "LightGBM с 5-фолдовой стратифицированной CV и ранней остановкой по AUC.",
        "about.p5": "Оценка",   "about.p5d": "Выдаём вероятность в [0, 1] на сигнал — ранжировано для триажа.",

        "err.too_many_files":  "Слишком много файлов (макс {n}).",
        "err.no_txn":          "Загрузите хотя бы один файл transactions CSV.",
        "err.empty_txn":       "В транзакционных данных нет строк.",
        "err.empty_sig":       "В данных сигналов нет строк.",
        "err.could_not_read":  "Не удалось прочитать {name}: {err}",
        "err.could_not_derive":"Не удалось извлечь сигналы: {err}",
        "err.pred_failed":     "Прогноз не выполнен: {err}",
    },

    # =====================================================================
    # UZBEK (Latin)
    # =====================================================================
    "uz": {
        "nav.home":         "Bosh sahifa",
        "nav.about":        "Haqida",
        "nav.dashboard":    "Boshqaruv paneli",
        "nav.predictions":  "Bashoratlar",
        "nav.predict":      "Sinab ko'ring",
        "nav.footer":       "EscalationLens · Xakaton uchun yaratilgan · LightGBM + Flask · ROC-AUC bo'yicha baholangan",

        "home.badge":           "Model ishlamoqda · ROC-AUC optimallashtirilgan",
        "home.title_1":         "Qaysi moliyaviy signallarni tekshirish",
        "home.title_2":         "kerakligini prognoz qiling.",
        "home.subtitle":        "EscalationLens tranzaksiyalar tarixini kalibrlangan eskalatsiya ehtimoliga aylantiradi — jamoangiz muhim signallarga vaqt ajratadi.",
        "home.cta_dashboard":   "📊 Panelni ochish",
        "home.cta_predictions": "🎯 Bashoratlarni ko'rish",
        "home.cta_about":       "📖 Qanday ishlaydi",

        "home.feat_eyebrow": "Imkoniyatlar",
        "home.feat_title":   "Xom tranzaksiyalardan tartiblangan signallargacha",
        "home.feat_sub":     "To'liq quvur: xususiyatlarni yaratish, gradient boosting va natijalar bilan ishlash uchun zamonaviy interfeys.",
        "home.f1_t": "Avtomatik xususiyat yaratish",
        "home.f1_d": "Tranzaksiyalar soni, summalari, yo'nalishi, xalqaro ulush, vaqt oynalari (1 soat → 7 kun) — barchasi har bir signal uchun.",
        "home.f2_t": "Gradient boosting",
        "home.f2_d": "LightGBM klassifikatori 5-qavatli stratifikatsiyalangan CV va erta to'xtash bilan. ROC-AUC bo'yicha baholanadi.",
        "home.f3_t": "Kalibrlangan ehtimollar",
        "home.f3_d": "Har bir signal [0, 1] oralig'ida ball oladi — triaj chegaralari yoki qo'lda ko'rib chiqish uchun tayyor.",
        "home.f4_t": "Tushunarli dizayn",
        "home.f4_d": "Xususiyat muhimligi reytingi model qaroriga qaysi naqshlar ta'sir qilganini ko'rsatadi.",
        "home.f5_t": "REST API",
        "home.f5_d": "Ballarni istalgan tizimga /api/predictions va /api/metrics orqali uzating.",
        "home.f6_t": "Tez va mustaqil",
        "home.f6_d": "Bitta Flask ilovasi, bitta o'qitilgan model, inferensda tashqi bog'liqlik yo'q.",
        "home.cta_title": "Ma'lumotlarni o'rganishga tayyormisiz?",
        "home.cta_desc":  "Interaktiv panelni ochib, eskalatsiya qilingan va rad etilgan signallar orasidagi farqni ko'ring.",
        "home.cta_btn":   "Panelni ochish →",

        "kpi.signals":            "Signallar",
        "kpi.transactions":       "Tranzaksiyalar",
        "kpi.escalation_rate":    "Eskalatsiya darajasi",
        "kpi.mean_prob":          "O'rtacha ehtimollik",
        "kpi.signals_analysed":   "Tahlil qilingan signallar",
        "kpi.historic_signals":   "tarixiy belgilangan signallar",
        "kpi.across_signals":     "barcha signallar bo'yicha",
        "kpi.of_signals":         "{b} dan {a}",
        "kpi.across_all":         "barcha signallar bo'yicha",
        "kpi.signals_scored":     "Baholangan signallar",
        "kpi.high_risk":          "Yuqori xavf (≥ 0.7)",
        "kpi.medium_risk":        "O'rta (0.3 – 0.7)",
        "kpi.low_risk":           "Past xavf (< 0.3)",
        "kpi.total_scored":       "Jami baholangan",
        "kpi.mean_prob_short":    "O'rtacha ehtimollik",
        "kpi.max_short":          "maks {p}",

        "band.escalate": "eskalatsiya",
        "band.review":   "ko'rib chiqish",
        "band.dismiss":  "rad etish",

        "predict.eyebrow":      "Modelni sinab ko'ring",
        "predict.title":        "Ma'lumotlaringizni yuklang",
        "predict.subtitle":     "Bir yoki bir nechta transactions.csv faylni (majburiy) va ixtiyoriy ravishda signals.csv fayllarni yuklang. Biz ularni birlashtirib, har bir signalni baholaymiz.",
        "predict.required":     "majburiy",
        "predict.optional":     "ixtiyoriy",
        "predict.dz_txn_title":"transactions.csv",
        "predict.dz_sig_title":"signals.csv",
        "predict.dz_txn_hint": "{n} tagacha CSV faylni bosing yoki sudrab tashlang",
        "predict.dz_sig_hint": "Bo'sh qoldirsangiz, har bir signal_id uchun signal yaratamiz",
        "predict.run":         "🚀 Bashoratni ishga tushirish",
        "predict.running":     "⏳ Model ishlamoqda…",
        "predict.note":        "{n} tagacha fayl · {mb} MB jami · Modelda {f} xususiyat",
        "predict.expected_title":"Kutilayotgan ustunlar",
        "predict.expected_txn":"transactions.csv (majburiy):",
        "predict.expected_sig":"signals.csv (ixtiyoriy):",
        "predict.expected_foot":"Yo'q ustunlar standart qiymatlar bilan to'ldiriladi. Umumiy taxalluslar (timestamp, transaction_id, date, type, …) avtomatik tanib olinadi.",
        "predict.success":     "✅ Bashorat tayyor",
        "predict.download":    "⬇️ predictions.csv ni yuklab olish",
        "predict.top_table":   "Eng xavfli 25 ta signal",
        "predict.showing":     "{n} tadan 25 tasi ko'rsatilmoqda — to'liq ro'yxat uchun CSV ni yuklab oling.",
        "predict.model_unavail":"Model mavjud emas.",
        "predict.error_prefix":"Xatolik:",

        "table.rank":        "#",
        "table.signal_id":   "Signal ID",
        "table.probability": "Ehtimollik",
        "table.band":        "Toifa",

        "pred.eyebrow":  "Model natijasi",
        "pred.title":    "Tartiblangan eskalatsiya ehtimollari",
        "pred.subtitle": "O'qitilgan LightGBM modeli tomonidan baholangan barcha signallar, xavf bo'yicha kamayish tartibida.",
        "pred.top20":    "Eng xavfli 20 ta signal",
        "pred.all":      "Barcha signallar (jami {n})",
        "pred.empty_t":  "Bashoratlar topilmadi",
        "pred.empty_d":  "predictions.csv yaratish uchun daftarni ishga tushiring.",
        "pred.api_t":    "Mashina o'qiy oladigan natija",
        "pred.api_d":    "Xuddi shu ma'lumotni /api/predictions orqali JSON sifatida oling.",

        "table.ground_truth": "Haqiqiy holat",
        "table.predicted":    "Bashorat",
        "table.match":        "Mos",

        "gt.escalated":  "1 · eskalatsiya",
        "gt.dismissed":  "0 · rad etilgan",

        "pred.acc_title":   "Modelning ushbu ma'lumotlardagi aniqligi",
        "pred.acc_line":    "0.5 chegarasida signallarning {p}% i to'g'ri tasniflandi",
        "pred.acc_correct": "✅ To'g'ri",
        "pred.acc_tp":      "To'g'ri ijobiy",
        "pred.acc_tp_sub":  "eskalatsiya — to'g'ri belgilangan",
        "pred.acc_fp":      "Xato ijobiy",
        "pred.acc_fp_sub":  "rad etilgan — lekin belgilangan",
        "pred.acc_fn":      "Xato salbiy",
        "pred.acc_fn_sub":  "eskalatsiya — lekin o'tkazib yuborilgan",

        "pred.chart_hist":   "Bashorat qilingan ehtimollik taqsimoti",
        "pred.chart_conf":   "Xatolar matritsasi (0.5 da)",
        "pred.cm_tp":        "To'g'ri ijobiy",
        "pred.cm_fp":        "Xato ijobiy",
        "pred.cm_tn":        "To'g'ri salbiy",
        "pred.cm_fn":        "Xato salbiy",
        "pred.cm_no_labels": "Haqiqiy belgilar mavjud emas",

        "dash.eyebrow":  "Jonli EDA",
        "dash.title":    "Ma'lumotlarni tadqiq etish",
        "dash.subtitle": "Model ortidagi tranzaksiya ma'lumotlarining interaktiv ko'rinishlari.",
        "dash.empty_t":  "Ma'lumot topilmadi",
        "dash.empty_d":  "data/signals.csv va data/transactions.csv mavjudligiga ishonch hosil qiling.",
        "dash.p_dir":    "Kiruvchi va Chiquvchi",
        "dash.p_types":  "Asosiy tranzaksiya turlari",
        "dash.p_amt":    "Summa taqsimoti (log1p)",
        "dash.p_evd":    "Sinf bo'yicha o'rtacha tranzaksiyalar",
        "dash.p_prob":   "Bashorat qilingan ehtimollik taqsimoti",

        "about.eyebrow":  "Loyiha haqida",
        "about.title":    "EscalationLens qanday ishlaydi",
        "about.subtitle": "Tranzaksiyalar oqimidan tekshirishga arziydigan signallar ro'yxatigacha.",
        "about.p1": "Yuklash",  "about.p1d": "signals.csv va transactions.csv fayllarini o'qish.",
        "about.p2": "Tadqiq",   "about.p2d": "Eskalatsiya va rad etilganlarni solishtirish: soni, summalari, yo'nalishi, davlat, vaqt.",
        "about.p3": "Xususiyat","about.p3d": "Har bir signal uchun ~50 xususiyat: agregatlar, nisbatlar, vaqt oynalari, one-hot turlar.",
        "about.p4": "O'qitish", "about.p4d": "LightGBM 5-qavatli stratifikatsiyalangan CV va AUC bo'yicha erta to'xtash bilan.",
        "about.p5": "Ballash",  "about.p5d": "Har bir signal uchun [0, 1] oraliqda ehtimollik — triaj uchun tartiblangan.",

        "err.too_many_files":  "Juda ko'p fayl (maks {n}).",
        "err.no_txn":          "Iltimos, kamida bitta transactions CSV yuklang.",
        "err.empty_txn":       "Tranzaksiya ma'lumotlarida qatorlar topilmadi.",
        "err.empty_sig":       "Signal ma'lumotlarida qatorlar topilmadi.",
        "err.could_not_read":  "{name} ni o'qib bo'lmadi: {err}",
        "err.could_not_derive":"Signallarni chiqarib bo'lmadi: {err}",
        "err.pred_failed":     "Bashorat amalga oshmadi: {err}",
    },
}


def get_translations(lang: str) -> dict:
    return TRANSLATIONS.get(lang) or TRANSLATIONS[DEFAULT_LANG]


def translate(lang: str, key: str, **kwargs) -> str:
    """Look up key in lang, fall back to English, fall back to key itself."""
    table = get_translations(lang)
    text = table.get(key)
    if text is None:
        text = TRANSLATIONS[DEFAULT_LANG].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text