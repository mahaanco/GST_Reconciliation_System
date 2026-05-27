import pandas as pd
from rapidfuzz import fuzz
from config import VALUE_TOLERANCE, MATCH_THRESHOLD


class GSTReconciliation:

    def __init__(self, purchase_df, gstr2b_df):
        self.purchase_df = purchase_df.copy()
        self.gstr2b_df = gstr2b_df.copy()

    def exact_match(self):

        merged = pd.merge(
            self.purchase_df,
            self.gstr2b_df,
            on=['GSTIN', 'INVOICE_NO'],
            how='outer',
            suffixes=('_BOOKS', '_2B'),
            indicator=True
        )

        merged['MATCH_STATUS'] = merged.apply(self.classify_match, axis=1)

        return merged

    def classify_match(self, row):

        if row['_merge'] == 'both':

            taxable_diff = abs(
                (row.get('TAXABLE_VALUE_BOOKS', 0) or 0)
                -
                (row.get('TAXABLE_VALUE_2B', 0) or 0)
            )

            gst_diff = abs(
                (row.get('GST_AMOUNT_BOOKS', 0) or 0)
                -
                (row.get('GST_AMOUNT_2B', 0) or 0)
            )
            if taxable_diff <= VALUE_TOLERANCE and gst_diff <= VALUE_TOLERANCE:
                return 'Perfect Match'
            else:
                return 'Value Mismatch'

        elif row['_merge'] == 'left_only':
            return 'Missing in 2B'

        elif row['_merge'] == 'right_only':
            return 'Missing in Books'

        return 'Unknown'

    def fuzzy_match(self):

        fuzzy_results = []
        unmatched_books = self.purchase_df.copy()
        unmatched_2b = self.gstr2b_df.copy()

        for _, book_row in unmatched_books.iterrows():

            best_score = 0
            best_match = None

            for _, gstr_row in unmatched_2b.iterrows():

                if book_row['GSTIN'] != gstr_row['GSTIN']:
                    continue

                score = fuzz.ratio(
                    str(book_row['INVOICE_NO']),
                    str(gstr_row['INVOICE_NO'])
                )
                if score > best_score:
                    best_score = score
                    best_match = gstr_row

            if best_score >= MATCH_THRESHOLD:
                fuzzy_results.append({
                    'GSTIN': book_row['GSTIN'],
                    'BOOK_INVOICE': book_row['INVOICE_NO'],
                    '2B_INVOICE': best_match['INVOICE_NO'],
                    'MATCH_SCORE': best_score,
                    'STATUS': 'Fuzzy Match'
                })

        return pd.DataFrame(fuzzy_results)

            
