import pandas as pd
import logging

from pii_hasher import PIIHasher


logging.basicConfig(
    filename='logs/processing.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)


class CancerRegistryPIIProcessor:

    def __init__(self):

        self.hasher = PIIHasher()

    def process_file(self, input_file, output_file):

        logging.info(f"Processing {input_file}")

        df = pd.read_csv(input_file)

        print(f"Records Loaded: {len(df)}")

        required_columns = [
            "site_id"
        ]

        for col in required_columns:

            if col not in df.columns:

                raise Exception(
                    f"Missing Required Column: {col}"
                )

        identifier_column = self.detect_identifier(df)

        df["delivery_patient_token"] = df.apply(
            lambda x: self.hasher.create_patient_token(
                x[identifier_column]
            ),
            axis=1
        )

        df["site_patient_id_hash"] = df.apply(
            lambda x: self.hasher.create_site_patient_hash(
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
            col for col in pii_columns
            if col in df.columns
        ]

        if len(existing_pii) > 0:

            df.drop(
                columns=existing_pii,
                inplace=True
            )

        df.to_csv(
            output_file,
            index=False
        )

        logging.info(
            f"Completed processing {len(df)} records"
        )

        print(
            f"Anonymized File Saved: {output_file}"
        )

    def detect_identifier(self, df):

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
            "No Patient Identifier Column Found"
        )
        
        
        
        
# import csv
# import os
# import logging

# from pii_hasher import PIIHasher

# logging.basicConfig(
#     filename='logs/processing.log',
#     level=logging.INFO,
#     format='%(asctime)s %(message)s'
# )

# class CancerRegistryPIIProcessor:

#     def __init__(self):
#         self.hasher = PIIHasher()

#     def process_file(self, input_file, output_file):
#         logging.info(f"Processing {input_file}")

#         # Check if file exists before running
#         if not os.path.exists(input_file):
#             raise FileNotFoundError(f"Input file not found: {input_file}")

#         # Open and load the entire CSV file into a list of dictionaries
#         with open(input_file, mode='r', encoding='utf-8', newline='') as infile:
#             reader = csv.DictReader(infile)
#             columns = reader.fieldnames if reader.fieldnames else []
#             rows = list(reader)

#         record_count = len(rows)
#         print(f"Records Loaded: {record_count}")

#         # 1. Check for required columns
#         required_columns = ["site_id"]
#         for col in required_columns:
#             if col not in columns:
#                 raise Exception(f"Missing Required Column: {col}")

#         # 2. Detect the patient identifier column
#         identifier_column = self.detect_identifier(columns)

#         # 3. Define PII columns to drop
#         pii_columns = {
#             "patient_id", "hospital_number", "medical_record_number",
#             "first_name", "middle_name", "last_name", "surname",
#             "full_name", "phone", "email", "national_id", "nin",
#             "passport_no", "address", "date_of_birth"
#         }

#         # 4. Filter the output header columns (drop PII, add new token/hash columns)
#         output_columns = [col for col in columns if col not in pii_columns]
#         output_columns.append("delivery_patient_token")
#         output_columns.append("site_patient_id_hash")

#         # 5. Process data row by row
#         processed_rows = []
#         for row in rows:
#             # Generate the new token and hash values
#             id_value = row[identifier_column]
#             site_id_value = row["site_id"]

#             delivery_token = self.hasher.create_patient_token(id_value)
#             site_hash = self.hasher.create_site_patient_hash(site_id_value, id_value)

#             # Build a new clean row containing only allowed columns + new hashes
#             new_row = {col: row[col] for col in columns if col not in pii_columns}
#             new_row["delivery_patient_token"] = delivery_token
#             new_row["site_patient_id_hash"] = site_hash

#             processed_rows.append(new_row)

#         # 6. Save the clean data to the output CSV
#         # Create output directory if it doesn't exist (e.g., inside an output folder)
#         output_dir = os.path.dirname(output_file)
#         if output_dir and not os.path.exists(output_dir):
#             os.makedirs(output_dir)

#         with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
#             writer = csv.DictWriter(outfile, fieldnames=output_columns)
#             writer.writeheader()
#             writer.writerows(processed_rows)

#         logging.info(f"Completed processing {record_count} records")
#         print(f"Anonymized File Saved: {output_file}")

#     def detect_identifier(self, columns):
#         candidates = [
#             "patient_id",
#             "hospital_number",
#             "medical_record_number",
#             "national_id",
#             "nin"
#         ]

#         for col in candidates:
#             if col in columns:
#                 return col

#         raise Exception("No Patient Identifier Column Found")
