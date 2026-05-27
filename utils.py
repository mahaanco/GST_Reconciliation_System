import pandas as pd
import re


def clean_invoice_number(invoice):
    if pd.isna(invoice):
        return ""

    invoice = str(invoice).upper().strip()
    invoice = re.sub(r'[^A-Z0-9]', '', invoice)

    return invoice
def clean_gstin(gstin):
    if pd.isna(gstin):
        return ""

    return str(gstin).upper().strip()


def clean_amount(value):
    try:
        return round(float(value), 2)
    except:
        return 0.0
def standardize_dataframe(df):

    df.columns = [col.strip().upper() for col in df.columns]

    column_mapping = {
        'GSTIN': 'GSTIN',
        'SUPPLIER GSTIN': 'GSTIN',
        'VENDOR GSTIN': 'GSTIN',
        'INVOICE NO': 'INVOICE_NO',
        'INVOICE NUMBER': 'INVOICE_NO',
        'INV NO': 'INVOICE_NO',
        'TAXABLE VALUE': 'TAXABLE_VALUE',
        'GST AMOUNT': 'GST_AMOUNT',
        'TOTAL GST': 'GST_AMOUNT',
        'INVOICE DATE': 'INVOICE_DATE'
    }
    df.rename(columns=column_mapping, inplace=True)

    required_columns = [
        'GSTIN',
        'INVOICE_NO',
        'INVOICE_DATE',
        'TAXABLE_VALUE',
        'GST_AMOUNT'
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    df['GSTIN'] = df['GSTIN'].apply(clean_gstin)
    df['INVOICE_NO'] = df['INVOICE_NO'].apply(clean_invoice_number)

    df['TAXABLE_VALUE'] = df['TAXABLE_VALUE'].apply(clean_amount)
    df['GST_AMOUNT'] = df['GST_AMOUNT'].apply(clean_amount)

    return df

