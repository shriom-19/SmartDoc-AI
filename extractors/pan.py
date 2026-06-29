import re

from extractors.common import CommonExtractor


class PANExtractor(CommonExtractor):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Main Extract Function
    # =====================================================

    def extract(self, text: str):

        text = self.clean_text(text)

        result = {}

        result["document_type"] = "pan"

        result["name"] = self.extract_name(text)

        result["father_name"] = self.extract_father_name(text)

        result["pan_number"] = self.extract_pan_number(text)

        result["dob"] = self.extract_dob(text)

        result["is_valid"] = self.is_valid_pan(text)

        result["raw_text"] = text

        return result

    # =====================================================
    # PAN Number
    # =====================================================

    def extract_pan_number(self, text):

        pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

        match = re.search(

            pattern,

            text.upper()

        )

        return match.group() if match else ""

    # =====================================================
    # Name
    # =====================================================

    def extract_name(self, text):

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        ignore = [

            "income tax department",

            "permanent account number",

            "government of india",

            "signature",

            "father",

            "date of birth",

            "pan",

            "income tax"

        ]

        for line in lines:

            lower = line.lower()

            if any(word in lower for word in ignore):

                continue

            if any(char.isdigit() for char in line):

                continue

            if len(line) < 4:

                continue

            if len(line.split()) >= 2:

                return line

        return ""

    # =====================================================
    # Father's Name
    # =====================================================

    def extract_father_name(self, text):

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        for i, line in enumerate(lines):

            if "father" in line.lower():

                if i + 1 < len(lines):

                    return lines[i + 1]

        return ""

    # =====================================================
    # DOB
    # =====================================================

    def extract_dob(self, text):

        patterns = [

            r"\d{2}/\d{2}/\d{4}",

            r"\d{2}-\d{2}-\d{4}",

            r"\d{2}\.\d{2}\.\d{4}"

        ]

        for pattern in patterns:

            match = re.search(

                pattern,

                text

            )

            if match:

                return match.group()

        return ""

    # =====================================================
    # PAN Validation
    # =====================================================

    def is_valid_pan(self, text):

        keywords = [

            "income tax department",

            "permanent account number",

            "government of india"

        ]

        lower = text.lower()

        score = sum(

            keyword in lower

            for keyword in keywords

        )

        return score >= 2