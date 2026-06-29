import re


class CommonExtractor:

    def __init__(self):
        pass

    # ======================================================
    # Clean OCR Text
    # ======================================================

    def clean_text(self, text):

        text = text.replace("|", "I")
        text = text.replace("||", " ")
        text = text.replace("—", "-")
        text = text.replace("–", "-")
        text = text.replace("“", '"')
        text = text.replace("”", '"')
        text = text.replace("‘", "'")
        text = text.replace("’", "'")

        # Preserve new lines
        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"\r", "", text)

        return text.strip()

    # ======================================================
    # Main Function
    # ======================================================

    def extract(self, text: str, document_type: str):

        text = self.clean_text(text)

        return {

            "document_type": document_type,

            "title": self.extract_title(text),

            "emails": self.extract_emails(text),

            "phone_numbers": self.extract_phone_numbers(text),

            "dates": self.extract_dates(text),

            "urls": self.extract_urls(text),

            "amounts": self.extract_amounts(text),

            "currency": self.extract_currency(text),

            "reference_numbers": self.extract_reference_numbers(text),

            "raw_text": text

        }

    # ======================================================
    # Title
    # ======================================================

    def extract_title(self, text):

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        return lines[0] if lines else ""

    # ======================================================
    # Emails
    # ======================================================

    def extract_emails(self, text):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        return list(

            set(

                re.findall(pattern, text)

            )

        )

    # ======================================================
    # Phone Numbers
    # ======================================================

    def extract_phone_numbers(self, text):

        pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}\b"

        return list(

            set(

                re.findall(pattern, text)

            )

        )

    # ======================================================
    # Dates
    # ======================================================

    def extract_dates(self, text):

        patterns = [

            r"\d{2}/\d{2}/\d{4}",

            r"\d{2}-\d{2}-\d{4}",

            r"\d{2}\.\d{2}\.\d{4}",

            r"\d{4}-\d{2}-\d{2}",

            r"\d{2}/\d{2}/\d{2}"

        ]

        dates = []

        for pattern in patterns:

            dates.extend(

                re.findall(

                    pattern,

                    text

                )

            )

        return list(set(dates))

    # ======================================================
    # URLs
    # ======================================================

    def extract_urls(self, text):

        pattern = r"(?:https?://|www\.)[^\s]+"

        return list(

            set(

                re.findall(

                    pattern,

                    text

                )

            )

        )

    # ======================================================
    # Amounts
    # ======================================================

    def extract_amounts(self, text):

        pattern = r"(?:₹|Rs\.?|INR)?\s?\d[\d,]*(?:\.\d{2})?"

        return list(

            set(

                re.findall(

                    pattern,

                    text

                )

            )

        )

    # ======================================================
    # Currency
    # ======================================================

    def extract_currency(self, text):

        if "₹" in text or "INR" in text.upper():

            return "INR"

        if "$" in text:

            return "USD"

        if "€" in text:

            return "EUR"

        return ""

    # ======================================================
    # GST Number
    # ======================================================

    def extract_gst(self, text):

        pattern = r"\d{2}[A-Z]{5}\d{4}[A-Z]\dZ[A-Z0-9]"

        match = re.search(

            pattern,

            text.upper()

        )

        return match.group() if match else ""

    # ======================================================
    # PIN Code
    # ======================================================

    def extract_pincode(self, text):

        pattern = r"\b\d{6}\b"

        return list(

            set(

                re.findall(

                    pattern,

                    text

                )

            )

        )

    # ======================================================
    # Percentage
    # ======================================================

    def extract_percentages(self, text):

        pattern = r"\d+(?:\.\d+)?%"

        return list(

            set(

                re.findall(

                    pattern,

                    text

                )

            )

        )

    # ======================================================
    # Reference Numbers
    # ======================================================

    def extract_reference_numbers(self, text):

        pattern = r"\b[A-Z0-9][A-Z0-9\-_/]{5,25}\b"

        return list(

            set(

                re.findall(

                    pattern,

                    text.upper()

                )

            )

        )