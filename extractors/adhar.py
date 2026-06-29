import re

from extractors.common import CommonExtractor


class AadhaarExtractor(CommonExtractor):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Main Extract Function
    # =====================================================

    def extract(self, text: str):

        text = self.clean_text(text)

        result = {}

        result["document_type"] = "adhar"

        result["name"] = self.extract_name(text)

        result["aadhaar_number"] = self.extract_aadhaar_number(text)

        result["dob"] = self.extract_dob(text)

        result["gender"] = self.extract_gender(text)

        result["address"] = self.extract_address(text)

        result["pincode"] = self.extract_pincode(text)

        result["emails"] = self.extract_emails(text)

        result["phone_numbers"] = self.extract_phone_numbers(text)

        result["is_valid"] = self.is_valid_aadhaar(text)

        result["raw_text"] = text.strip()

        return result

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

            "government",

            "india",

            "aadhaar",

            "uidai",

            "unique identification authority",

            "dob",

            "date of birth",

            "year of birth",

            "male",

            "female",

            "address"

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
    # Aadhaar Number
    # =====================================================

    def extract_aadhaar_number(self, text):

        pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

        match = re.search(

            pattern,

            text

        )

        if match:

            return " ".join(

                match.group().split()

            )

        return ""

    # =====================================================
    # DOB
    # =====================================================

    def extract_dob(self, text):

        patterns = [

            r"DOB[: ]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",

            r"Date\s*of\s*Birth[: ]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",

            r"Year\s*of\s*Birth[: ]*([0-9]{4})",

            r"\b([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})\b"

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

    # =====================================================
    # Gender
    # =====================================================

    def extract_gender(self, text):

        lower = text.lower()

        if re.search(r"\bfemale\b", lower):

            return "Female"

        if re.search(r"\bmale\b", lower):

            return "Male"

        return ""

    # =====================================================
    # Address
    # =====================================================

    def extract_address(self, text):

        lines = text.split("\n")

        address = []

        capture = False

        stop_words = [

            "government",

            "uidai",

            "aadhaar",

            "www",

            "help",

            "phone",

            "email",

            "support",

            "1947"

        ]

        for line in lines:

            lower = line.lower()

            if "address" in lower:

                capture = True

                continue

            if capture:

                if any(

                    word in lower

                    for word in stop_words

                ):

                    break

                if line.strip():

                    address.append(

                        line.strip()

                    )

        return " ".join(address)

    # =====================================================
    # Aadhaar Validation
    # =====================================================

    def is_valid_aadhaar(self, text):

        keywords = [

            "government of india",

            "unique identification authority",

            "aadhaar",

            "uidai"

        ]

        lower = text.lower()

        score = sum(

            keyword in lower

            for keyword in keywords

        )

        return score >= 2