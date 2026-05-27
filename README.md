# GST Reconciliation Automation System

A production-ready GST reconciliation platform built using Python and Streamlit for automating GSTR-2B vs Purchase Register reconciliation.

---

# Features

- GSTR-2B vs Purchase Register reconciliation
- Exact invoice matching
- Fuzzy invoice matching
- Value mismatch detection
- Missing invoice identification
- GSTIN standardization
- Dashboard analytics
- Excel report export
- Streamlit-based UI
- Production-ready modular architecture

---

# Project Structure

```bash
GST_Reconciliation_System/
│
├── app.py
├── reconciliation_engine.py
├── report_generator.py
├── utils.py
├── database.py
├── config.py
├── requirements.txt
├── uploads/
├── exports/
└── README.md
```

---

# Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- RapidFuzz
- SQLAlchemy
- XlsxWriter

---

# Installation

## Clone Repository

```bash
git clone <your-repository-url>
cd GST_Reconciliation_System
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
streamlit run app.py
```

---

# Input File Requirements

## Purchase Register Columns

Required columns:

- GSTIN
- Invoice No
- Invoice Date
- Taxable Value
- GST Amount

---

## GSTR-2B Columns

Required columns:

- GSTIN
- Invoice No
- Invoice Date
- Taxable Value
- GST Amount

---

# Reconciliation Categories

| Category | Description |
|---|---|
| Perfect Match | Invoice matched successfully |
| Value Mismatch | Invoice exists but values differ |
| Missing in 2B | Present in books but absent in GSTR-2B |
| Missing in Books | Present in GSTR-2B but absent in books |
| Fuzzy Match | Similar invoice detected using fuzzy logic |

---

# Features Explained

## Exact Matching

Matches invoices using:

- GSTIN
- Invoice Number

with configurable tolerance for value differences.

---

## Fuzzy Matching

Uses RapidFuzz similarity scoring to identify:

- Invoice formatting differences
- Typographical variations
- Minor invoice mismatches

Example:

```text
INV001
INV-001
INV / 001
```

---

# Dashboard Analytics

Includes:

- Match summary
- Pie chart analytics
- Exception reporting
- Reconciliation statistics

---

# Excel Export

Generated report includes:

- Reconciliation Sheet
- Fuzzy Match Sheet
- Summary Report

---

# Configuration

Update values in `config.py`

```python
MATCH_THRESHOLD = 90
VALUE_TOLERANCE = 5
```

---

# Recommended Future Enhancements

## Phase 2

- Multi-client support
- PostgreSQL integration
- User authentication
- Vendor compliance scoring
- Auto email reminders
- GSTIN API validation
- AI-generated commentary

---

## Phase 3

- Tally integration
- SAP integration
- ERP connectors
- Cloud deployment
- SaaS architecture
- AI compliance assistant

---

# Deployment Options

Recommended platforms:

- AWS
- Azure
- GCP
- Render
- Railway

---

# Commercial Use Cases

This solution can be used for:

- CA firms
- CFO advisory services
- GST outsourcing firms
- SMEs
- Internal finance teams
- Shared service centers

---

# License

This project is intended for internal and commercial business automation purposes.
