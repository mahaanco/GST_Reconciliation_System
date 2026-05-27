import pandas as pd
import re


# ==========================================
# CLEAN INVOICE NUMBER
# ==========================================
def clean_invoice_number(invoice):

    if pd.isna(invoice):

        return ""

    invoice = str(invoice).upper().strip()

    # REMOVE SPECIAL CHARACTERS
    invoice = re.sub(
        r'[^A-Z0-9]',
        '',
        invoice
    )

    return invoice


# ==========================================
# CLEAN GSTIN
# ==========================================
def clean_gstin(gstin):

    if pd.isna(gstin):

        return ""

    return str(gstin).upper().strip()


# ==========================================
# CLEAN NUMERIC AMOUNTS
# ==========================================
def clean_amount(value):

    try:

        # REMOVE COMMAS
        value = str(value).replace(',', '')

        return round(
            float(value),
            2
        )

    except:

        return 0.0


# ==========================================
# STANDARDIZE DATAFRAME
# ==========================================
def standardize_dataframe(df):

    # CLEAN COLUMN NAMES
    df.columns = [

        str(col).strip().upper()

        for col in df.columns
    ]

    # ==========================================
    # COLUMN MAPPING
    # ==========================================
    column_mapping = {

        # GSTIN
        'GSTIN': 'GSTIN',
        'GSTIN/UIN': 'GSTIN',
        'GSTIN OF SUPPLIER': 'GSTIN',
        'SUPPLIER GSTIN': 'GSTIN',
        'VENDOR GSTIN': 'GSTIN',

        # INVOICE NUMBER
        'INVOICE NO': 'INVOICE_NO',
        'INVOICE NUMBER': 'INVOICE_NO',
        'INV NO': 'INVOICE_NO',
        'SUPPLIER INVOICE NO.': 'INVOICE_NO',
        'INVOICE NUMBER ': 'INVOICE_NO',

        # INVOICE DATE
        'INVOICE DATE': 'INVOICE_DATE',
        'INVOICE DATE ': 'INVOICE_DATE',

        # TAXABLE VALUE
        'TAXABLE VALUE': 'TAXABLE_VALUE',
        'TAXABLE VALUE(₹)': 'TAXABLE_VALUE',
        'VALUE': 'TAXABLE_VALUE',

        # GST AMOUNT
        'GST AMOUNT': 'GST_AMOUNT',
        'TOTAL GST': 'GST_AMOUNT',

        # GST BREAKUP
        'IGST': 'IGST',
        'CGST': 'CGST',
        'SGST': 'SGST',

        'IGST(₹)': 'IGST',
        'CGST(₹)': 'CGST',
        'SGST(₹)': 'SGST'
    }

    # RENAME COLUMNS
    df.rename(
        columns=column_mapping,
        inplace=True
    )

    # ==========================================
    # REQUIRED COLUMNS
    # ==========================================
    required_columns = [

        'GSTIN',
        'INVOICE_NO',
        'INVOICE_DATE',
        'TAXABLE_VALUE',
        'GST_AMOUNT',
        'IGST',
        'CGST',
        'SGST'
    ]

    # CREATE MISSING COLUMNS
    for col in required_columns:

        if col not in df.columns:

            df[col] = 0

    # ==========================================
    # CLEAN TEXT COLUMNS
    # ==========================================
    df['GSTIN'] = df['GSTIN'].apply(
        clean_gstin
    )

    df['INVOICE_NO'] = df[
        'INVOICE_NO'
    ].apply(
        clean_invoice_number
    )

    # ==========================================
    # CLEAN NUMERIC COLUMNS
    # ==========================================
    numeric_columns = [

        'TAXABLE_VALUE',
        'GST_AMOUNT',
        'IGST',
        'CGST',
        'SGST'
    ]

    for col in numeric_columns:

        df[col] = df[col].apply(
            clean_amount
        )

    # ==========================================
    # CREATE GST_AMOUNT
    # IF GST BREAKUP EXISTS
    # ==========================================
    if (

        df['GST_AMOUNT'].sum() == 0

    ):

        df['GST_AMOUNT'] = (

            df['IGST']
            +
            df['CGST']
            +
            df['SGST']

        )

    # ==========================================
    # REMOVE EMPTY GSTIN
    # ==========================================
    df = df[

        df['GSTIN'] != ''

    ]

    # ==========================================
    # REMOVE EMPTY INVOICE
    # ==========================================
    df = df[

        df['INVOICE_NO'] != ''

    ]

    # ==========================================
    # REMOVE TOTAL ROWS
    # ==========================================
    df = df[

        ~df['GSTIN'].astype(str).str.contains(
            'TOTAL',
            case=False,
            na=False
        )

    ]

    # ==========================================
    # REMOVE DUPLICATES
    # ==========================================
    df = df.drop_duplicates(

        subset=[
            'GSTIN',
            'INVOICE_NO',
            'GST_AMOUNT'
        ]

    )

    # RESET INDEX
    df.reset_index(
        drop=True,
        inplace=True
    )

    return df
