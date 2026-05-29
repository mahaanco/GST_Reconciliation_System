# GST Reconciliation System

A Streamlit-based GST Reconciliation application for comparing Purchase Registers, Sales Registers, GSTR-2B, and GSTR-1 data.

## Features

* Purchase Register vs GSTR-2B Reconciliation
* Sales Register vs GSTR-1 Reconciliation
* Automatic Column Mapping
* GSTIN Validation
* Invoice Number Standardization
* Exact Matching
* Fuzzy Invoice Matching
* Amount Variance Detection
* Date Variance Detection
* Duplicate Invoice Detection
* Excel Report Generation
* Streamlit Dashboard
* Downloadable Reconciliation Reports

## Supported File Formats

* XLSX
* XLS
* CSV

## Project Structure

```text
gst-reconciliation/

├── app.py
├── requirements.txt
│
├── .streamlit/
│   └── config.toml
│
├── config/
│   └── mapping.json
│
├── core/
│   ├── cleaner.py
│   ├── validator.py
│   ├── mapper.py
│   ├── matcher.py
│   ├── duplicate_detector.py
│   ├── fuzzy_matcher.py
│   └── reconciler.py
│
├── parsers/
│   ├── excel_parser.py
│   ├── csv_parser.py
│   └── file_reader.py
│
├── services/
│   ├── upload_service.py
│   └── reconciliation_service.py
│
├── reports/
│   ├── summary.py
│   └── excel_report.py
│
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd gst-reconciliation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Deployment

This application can be deployed directly on Streamlit Community Cloud.

### Steps

1. Push the project to GitHub.
2. Login to Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the repository.
5. Set the main file path as:

```text
app.py
```

6. Deploy the application.

## Reconciliation Workflow

1. Upload Source File
2. Upload Target File
3. Configure Matching Parameters
4. Run Reconciliation
5. Review Results
6. Download Excel Report

## Generated Report Sheets

* Summary
* Matched
* Missing In Target
* Missing In Source
* Amount Mismatch
* Date Mismatch
* Fuzzy Matches
* Source Duplicates
* Target Duplicates

## Matching Logic

### Exact Match

* GSTIN
* Invoice Number

### Fuzzy Match

Used when invoice numbers differ slightly.

Example:

```text
INV001
INV-001
```

### Amount Validation

Configurable tolerance-based matching.

### Date Validation

Configurable date tolerance matching.

## Future Enhancements

* Multi-sheet Excel Support
* PDF Support
* OCR Support
* Vendor Compliance Dashboard
* GSTR-2A Reconciliation
* Books vs GSTR-3B Reconciliation
* E-Invoice Reconciliation
* E-Way Bill Reconciliation
* Multi-Client Management

## License

This project is intended for internal business use.
