import pandas as pd
from rapidfuzz import fuzz
from config import VALUE_TOLERANCE, MATCH_THRESHOLD


class GSTReconciliation:

    def __init__(self, purchase_df, gstr2b_df):

        self.purchase_df = purchase_df.copy()
        self.gstr2b_df = gstr2b_df.copy()

    # ==========================================
    # EXACT MATCHING
    # ==========================================
    def exact_match(self):

        merged = pd.merge(
            self.purchase_df,
            self.gstr2b_df,
            on=['GSTIN', 'INVOICE_NO'],
            how='outer',
            suffixes=('_BOOKS', '_2B'),
            indicator=True
        )

        # APPLY MATCH CLASSIFICATION
        merged['MATCH_STATUS'] = merged.apply(
            self.classify_match,
            axis=1
        )

        return merged

    # ==========================================
    # CLASSIFY MATCHES
    # ==========================================
    def classify_match(self, row):

        # MISSING IN 2B
        if row['_merge'] == 'left_only':

            return 'Missing in 2B'

        # MISSING IN BOOKS
        elif row['_merge'] == 'right_only':

            return 'Missing in Books'

        # BOTH FOUND
        elif row['_merge'] == 'both':

            # SAFE NUMERIC CONVERSION
            taxable_books = pd.to_numeric(
                row.get(
                    'TAXABLE_VALUE_BOOKS',
                    0
                ),
                errors='coerce'
            )

            taxable_2b = pd.to_numeric(
                row.get(
                    'TAXABLE_VALUE_2B',
                    0
                ),
                errors='coerce'
            )

            gst_books = pd.to_numeric(
                row.get(
                    'GST_AMOUNT_BOOKS',
                    0
                ),
                errors='coerce'
            )

            gst_2b = pd.to_numeric(
                row.get(
                    'GST_AMOUNT_2B',
                    0
                ),
                errors='coerce'
            )

            # HANDLE NAN VALUES
            taxable_books = 0 if pd.isna(
                taxable_books
            ) else taxable_books

            taxable_2b = 0 if pd.isna(
                taxable_2b
            ) else taxable_2b

            gst_books = 0 if pd.isna(
                gst_books
            ) else gst_books

            gst_2b = 0 if pd.isna(
                gst_2b
            ) else gst_2b

            # CALCULATE DIFFERENCE
            taxable_diff = abs(
                taxable_books - taxable_2b
            )

            gst_diff = abs(
                gst_books - gst_2b
            )

            # PERFECT MATCH
            if (
                taxable_diff <= VALUE_TOLERANCE
                and
                gst_diff <= VALUE_TOLERANCE
            ):

                return 'Perfect Match'

            # PARTIAL MATCH
            elif (
                taxable_diff <= 100
                or
                gst_diff <= 100
            ):

                return 'Partial Match'

            # VALUE MISMATCH
            else:

                return 'Value Mismatch'

        return 'Unknown'

    # ==========================================
    # FUZZY MATCHING
    # ==========================================
    def fuzzy_match(self):

        fuzzy_results = []

        # ONLY UNMATCHED RECORDS
        unmatched_books = self.purchase_df.copy()

        unmatched_2b = self.gstr2b_df.copy()

        for _, book_row in unmatched_books.iterrows():

            best_score = 0
            best_match = None

            for _, gstr_row in unmatched_2b.iterrows():

                # GSTIN MUST MATCH
                if (
                    str(book_row['GSTIN']).strip()
                    !=
                    str(gstr_row['GSTIN']).strip()
                ):

                    continue

                # INVOICE FUZZY SCORE
                score = fuzz.ratio(
                    str(
                        book_row['INVOICE_NO']
                    ),
                    str(
                        gstr_row['INVOICE_NO']
                    )
                )

                if score > best_score:

                    best_score = score
                    best_match = gstr_row

            # FUZZY MATCH FOUND
            if (
                best_score >= MATCH_THRESHOLD
                and
                best_match is not None
            ):

                # VALUE VALIDATION
                taxable_diff = abs(
                    pd.to_numeric(
                        book_row.get(
                            'TAXABLE_VALUE',
                            0
                        ),
                        errors='coerce'
                    )
                    -
                    pd.to_numeric(
                        best_match.get(
                            'TAXABLE_VALUE',
                            0
                        ),
                        errors='coerce'
                    )
                )

                gst_diff = abs(
                    pd.to_numeric(
                        book_row.get(
                            'GST_AMOUNT',
                            0
                        ),
                        errors='coerce'
                    )
                    -
                    pd.to_numeric(
                        best_match.get(
                            'GST_AMOUNT',
                            0
                        ),
                        errors='coerce'
                    )
                )

                fuzzy_results.append({

                    'GSTIN':
                    book_row['GSTIN'],

                    'BOOK_INVOICE':
                    book_row['INVOICE_NO'],

                    '2B_INVOICE':
                    best_match['INVOICE_NO'],

                    'MATCH_SCORE':
                    best_score,

                    'BOOK_TAXABLE':
                    book_row.get(
                        'TAXABLE_VALUE',
                        0
                    ),

                    '2B_TAXABLE':
                    best_match.get(
                        'TAXABLE_VALUE',
                        0
                    ),

                    'BOOK_GST':
                    book_row.get(
                        'GST_AMOUNT',
                        0
                    ),

                    '2B_GST':
                    best_match.get(
                        'GST_AMOUNT',
                        0
                    ),

                    'TAXABLE_DIFF':
                    taxable_diff,

                    'GST_DIFF':
                    gst_diff,

                    'STATUS':
                    'Fuzzy Match'
                })

        return pd.DataFrame(
            fuzzy_results
        )
