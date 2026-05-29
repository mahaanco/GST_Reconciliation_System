import json


class ColumnMapper:

    def __init__(
        self,
        mapping_file
    ):

        with open(
            mapping_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.mapping = (
                json.load(f)
            )

    @staticmethod
    def normalize(
        column_name
    ):

        return (
            str(column_name)
            .lower()
            .strip()
        )

    def map_columns(
        self,
        df
    ):

        detected = {}

        normalized_columns = {
            self.normalize(col): col
            for col in df.columns
        }

        for (
            standard_name,
            aliases
        ) in self.mapping.items():

            detected[
                standard_name
            ] = None

            for alias in aliases:

                alias = (
                    alias
                    .lower()
                    .strip()
                )

                if (
                    alias
                    in
                    normalized_columns
                ):

                    detected[
                        standard_name
                    ] = (
                        normalized_columns[
                            alias
                        ]
                    )

                    break

        return detected

    @staticmethod
    def validate_mapping(
        mapped_columns
    ):

        mandatory = [
            "gstin",
            "invoice_number"
        ]

        missing = []

        for col in mandatory:

            if (
                mapped_columns.get(
                    col
                )
                is None
            ):
                missing.append(
                    col
                )

        return missing
