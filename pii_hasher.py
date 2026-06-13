import hashlib
import os
from config import SALT_FILE


class PIIHasher:

    def __init__(self):
        self.salt = self.load_salt()

    def load_salt(self):

        if not os.path.exists(SALT_FILE):

            random_salt = os.urandom(32).hex()

            with open(SALT_FILE, "w") as f:
                f.write(random_salt)

        with open(SALT_FILE, "r") as f:
            return f.read().strip()

    def hash_value(self, value):

        if value is None:
            value = ""

        value = str(value).strip().lower()

        combined = self.salt + value

        return hashlib.sha256(
            combined.encode("utf-8")
        ).hexdigest()

    def create_patient_token(self, patient_identifier):

        return self.hash_value(patient_identifier)

    def create_site_patient_hash(self, site_id, patient_identifier):

        combined = f"{site_id}|{patient_identifier}"

        return self.hash_value(combined)
