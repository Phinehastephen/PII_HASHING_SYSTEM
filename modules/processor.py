import pandas as pd

from modules.hashing import PIIHasher


class CancerRegistryPIIProcessor:

    def __init__(self):

        self.hasher = PIIHasher()

    def detect_identifier(
        self,
        df
    ):

        candidates = [

            "patient_id",

            "hospital_number",

            "medical_record_number",

            "national_id",

            "nin"

        ]

        for col in candidates:

            if col in df.columns:
                return col

        raise Exception(
            "No patient identifier found."
        )

    def process_file(
        self,
        input_file,
        output_file
    ):

        df = pd.read_csv(
            input_file
        )

        if "site_id" not in df.columns:

            raise Exception(
                "site_id column missing."
            )

        identifier_column = (
            self.detect_identifier(df)
        )

        df[
            "delivery_patient_token"
        ] = df.apply(
            lambda x:
            self.hasher.create_patient_token(
                x[identifier_column]
            ),
            axis=1
        )

        df[
            "site_patient_id_hash"
        ] = df.apply(
            lambda x:
            self.hasher.create_site_patient_hash(
                x["site_id"],
                x[identifier_column]
            ),
            axis=1
        )

        pii_columns = [

            "patient_id",

            "hospital_number",

            "medical_record_number",

            "first_name",

            "middle_name",

            "last_name",

            "surname",

            "full_name",

            "phone",

            "email",

            "national_id",

            "nin",

            "passport_no",

            "address",

            "date_of_birth"

        ]

        existing_pii = [

            col

            for col in pii_columns

            if col in df.columns

        ]

        if existing_pii:

            df.drop(
                columns=existing_pii,
                inplace=True
            )

        df.to_csv(
            output_file,
            index=False
        )

        return {
            "records_processed":
            len(df),

            "records_hashed":
            len(df),

            "removed_columns":
            existing_pii
        }