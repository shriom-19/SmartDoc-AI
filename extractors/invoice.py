import re

from extractors.common import CommonExtractor


class InvoiceExtractor(CommonExtractor):

    def __init__(self):

        super().__init__()

    # ======================================================
    # Main Function
    # ======================================================

    def extract(self, text: str):

        text = self.clean_text(text)

        result = {}

        result["document_type"] = "invoice"

        result["vendor"] = self.extract_vendor(text)

        result["invoice_number"] = self.extract_invoice_number(text)

        result["invoice_date"] = self.extract_invoice_date(text)

        result["gst_number"] = self.extract_gst(text)

        result["total_amount"] = self.extract_total_amount(text)

        result["emails"] = self.extract_emails(text)

        result["phone_numbers"] = self.extract_phone_numbers(text)

        result["dates"] = self.extract_dates(text)

        result["raw_text"] = text

        return result

    # ======================================================
    # Vendor
    # ======================================================

    def extract_vendor(self, text):

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        ignore = [

            "invoice",

            "tax invoice",

            "bill",

            "gst",

            "gstin",

            "invoice no",

            "invoice number",

            "invoice date",

            "date",

            "total",

            "amount",

            "qty",

            "quantity",

            "description",

            "price"

        ]

        for line in lines:

            lower = line.lower()

            if any(word in lower for word in ignore):

                continue

            if any(char.isdigit() for char in line):

                continue

            if len(line) > 3:

                return line

        return ""

    # ======================================================
    # Invoice Number
    # ======================================================

    def extract_invoice_number(self, text):

        patterns = [

            r"Invoice\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Invoice\s*Number\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Inv\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Bill\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Bill\s*Number\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

            r"Document\s*No\.?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                return match.group(1)

        return ""

    # ======================================================
    # Invoice Date
    # ======================================================

    def extract_invoice_date(self, text):

        patterns = [

            r"Invoice\s*Date\s*[:\-]?\s*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",

            r"Date\s*[:\-]?\s*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",

            r"Dated\s*[:\-]?\s*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                return match.group(1)

        dates = self.extract_dates(text)

        return dates[0] if dates else ""

    # ======================================================
    # Total Amount
    # ======================================================

    def extract_total_amount(self, text):

        patterns = [

            r"Grand\s*Total\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Total\s*Amount\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Invoice\s*Total\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Net\s*Amount\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Amount\s*Payable\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Balance\s*Due\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Total\s*Due\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)",

            r"Total\s*[:\-]?\s*₹?\s*([\d,]+(?:\.\d{2})?)"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                return match.group(1)

        amounts = self.extract_amounts(text)

        return amounts[-1] if amounts else ""