# Automated Data Quality Pipeline

A reusable Python data-validation pipeline with a Streamlit monitoring interface. It profiles CSV data, applies configurable quality rules and produces an exception report.

## Checks
- Missing required values
- Duplicate business keys
- Numeric range violations
- Invalid email formats
- Invalid or future dates
- Overall quality score and row-level exceptions

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
pytest
```

## Use case
Data analysts can run this gate before dashboard refreshes or database loads to prevent unreliable records from reaching reports.

## Technology
Python · pandas · Streamlit · Plotly · pytest

The rules engine and demonstration data are original portfolio work.
