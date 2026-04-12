# Retail Customer & Revenue Analysis

An end-to-end data analysis project using the UCI Online Retail II dataset.
Built as a portfolio project to practise the full analytics stack: data cleaning,
exploratory analysis, customer segmentation and dashboard delivery — structured
as if commissioned by an internal Finance team.

---

## Project brief

> _Which customer segments are driving revenue, which products are driving
> cancellations, and what should the commercial team prioritise next quarter?_

Full brief: [`docs/brief-RET001.md`](docs/brief-RET001.md) _(coming soon)_

---

## Dataset

**UCI Online Retail II** — ~1 million transactions from a UK-based online gift
retailer, December 2009 to December 2011.

- Source: [archive.ics.uci.edu/dataset/502](https://archive.ics.uci.edu/dataset/502)
- Downloaded via `kagglehub` — not committed to this repo
- See `data/` for folder structure; raw data is gitignored

---

## Structure

```
retail-analysis/
├── src/                # reusable modules
│   ├── load.py         # data loading and type coercion
│   ├── clean.py        # cleaning logic and decisions
│   └── analysis/
│       ├── revenue.py   # net revenue after cancellations (Q1)
│       ├── customers.py # RFM segmentation, cohort retention (Q2, Q3)
│       ├── products.py  # cancellation rates by product (Q4)
│       └── segments.py  # customer segment definitions (Q6)
├── notebooks/          # analysis notebooks, one per question
├── tests/              # pytest unit tests for core logic
├── data/               # gitignored — not committed
└── requirements.txt
```

---

## Setup

### Windows

```powershell
venv\Scripts\activate
$env:PYTHONPATH="."
pytest tests/ -v
```

### Mac/Linux

```bash
source venv/bin/activate
PYTHONPATH=. pytest tests/ -v
```

### Jupyter venv install for failing VScode

```python
import subprocess
import sys

subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
```

You will need a Kaggle account to download the dataset. The `load.py` module
handles this via `kagglehub` — follow the
[kagglehub setup instructions](https://github.com/Kaggle/kagglehub) to
configure your credentials.

---

## Analysis questions

| #   | Question                                     | Module         | Status         |
| --- | -------------------------------------------- | -------------- | -------------- |
| Q1  | Net revenue after cancellations              | `revenue.py`   | ✅ Complete    |
| Q2  | Revenue concentration — top 20% of customers | `customers.py` | ✅ Complete    |
| Q3  | Customer retention curve                     | `customers.py` | ✅ Complete    |
| Q4  | Product cancellation rates                   | `products.py`  | 🔄 In progress |
| Q5  | Seasonal patterns and anomalies              | `revenue.py`   | ⬜ Pending     |
| Q6  | Customer segmentation                        | `segments.py`  | ⬜ Pending     |

---

## Key findings

- **Net revenue: £18.9m** against £19.6m gross — a 7.2% cancellation rate representing ~£670k in lost revenue
- **Seasonal pattern is pronounced** — November peaks in both years (~2× a typical month), driven by Christmas wholesale orders
- **Two anomalous cancellation spikes** Two cancellation spikes in January 2011 (13.65%) and December 2011 (28.51%) are attributable to single anomalous transactions — likely data entry errors — rather than systemic operational issues. Excluding these two invoices, the underlying cancellation rate is approximately 2–3% and consistent across both years.
- **Cancellation rate of 7.2%** Excluding two data entry errors, the true underlying rate is 2.4% — representing approximately £470k in genuine lost revenue against £19.6m gross. This is within normal range for a gift retailer of this type.
- **Revenue is highly concentrated** — the top 20% of customers (1,170 of 5,840) generate 76.7% of total revenue. Losing a small number of high-value customers would have a disproportionate impact on the business.
- **Retention stabilises quickly** — average monthly retention sits at ~20% across all periods, suggesting the identified customer base is predominantly repeat wholesale buyers rather than casual consumers.
- **One-time buyers represent only 1.7% of identified customers** — however this excludes ~235k guest transactions which are likely disproportionately one-time purchasers, meaning the true rate is significantly higher.

---

## Stack

- **Python** — pandas, numpy, matplotlib, seaborn
- **Git** — full version history with conventional commits
- **Power BI / Tableau** — dashboard _(coming in phase 2)_
- **dbt** — data modelling layer _(planned for months 7–8)_

---

## Status

Work in progress — building over an 11-month period alongside full-time employment
as part of a deliberate upskilling plan targeting senior analytics roles in the UK.
