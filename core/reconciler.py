def reconcile(
    self,
    source_df,
    target_df,

    source_gstin_col,
    target_gstin_col,

    source_invoice_col,
    target_invoice_col,

    source_amount_col=None,
    target_amount_col=None,

    source_date_col=None,
    target_date_col=None
):

    source_df = (
        ExactMatcher
        .create_match_key(
            source_df,
            source_gstin_col,
            source_invoice_col
        )
    )

    target_df = (
        ExactMatcher
        .create_match_key(
            target_df,
            target_gstin_col,
            target_invoice_col
        )
    )

    source_duplicates = (
        DuplicateDetector
        .detect(
            source_df
        )
    )

    target_duplicates = (
        DuplicateDetector
        .detect(
            target_df
        )
    )

    (
        matched,
        source_only,
        target_only
    ) = (
        ExactMatcher.match(
            source_df,
            target_df
        )
    )

    amount_mismatch = (
        self._check_amount_mismatch(
            matched,
            target_df,
            source_amount_col
        )
        if source_amount_col
        else pd.DataFrame()
    )

    date_mismatch = (
        self._check_date_mismatch(
            matched,
            target_df,
            source_date_col
        )
        if source_date_col
        else pd.DataFrame()
    )

    fuzzy_matches = (
        FuzzyMatcher.match(
            source_only,
            target_only,
            source_gstin_col,
            source_invoice_col,
            self.fuzzy_threshold
        )
    )

    return {

        "matched":
            matched,

        "source_only":
            source_only,

        "target_only":
            target_only,

        "amount_mismatch":
            amount_mismatch,

        "date_mismatch":
            date_mismatch,

        "fuzzy_matches":
            fuzzy_matches,

        "source_duplicates":
            source_duplicates,

        "target_duplicates":
            target_duplicates
    }
