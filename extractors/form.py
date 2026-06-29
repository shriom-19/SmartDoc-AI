import re

from extractors.common import CommonExtractor


class FormExtractor(CommonExtractor):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Main Extract Function
    # =====================================================

    def extract(self, text: str):

        text = self.clean_text(text)

        result = {}

        result["document_type"] = "form"

        result["fields"] = self.extract_key_value_pairs(text)

        result["emails"] = self.extract_emails(text)

        result["phone_numbers"] = self.extract_phone_numbers(text)

        result["dates"] = self.extract_dates(text)

        result["raw_text"] = text

        return result

    # =====================================================
    # Key : Value Extraction
    # =====================================================

    def extract_key_value_pairs(self, text):

        fields = {}

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        for line in lines:

            # ------------------------------------------
            # Name : Rahul
            # ------------------------------------------

            if ":" in line:

                key, value = line.split(":", 1)

            # ------------------------------------------
            # Name - Rahul
            # Avoid dates like 01-01-2025
            # ------------------------------------------

            elif " - " in line:

                key, value = line.split(" - ", 1)

            else:

                continue

            key = key.strip()

            value = value.strip()

            if key and value:

                fields[key] = value

        return fields