import re

from extractors.common import CommonExtractor


class ResumeExtractor(CommonExtractor):

    def __init__(self):

        super().__init__()

    # ======================================================
    # Main Extract Function
    # ======================================================

    def extract(self, text: str):

        text = self.clean_text(text)

        result = {}

        result["document_type"] = "resume"

        result["name"] = self.extract_name(text)

        result["emails"] = self.extract_emails(text)

        result["phone_numbers"] = self.extract_phone_numbers(text)

        result["skills"] = self.extract_skills(text)

        result["education"] = self.extract_education(text)

        result["experience"] = self.extract_experience(text)

        result["raw_text"] = text

        return result

    # ======================================================
    # Name
    # ======================================================

    def extract_name(self, text):

        lines = [

            line.strip()

            for line in text.split("\n")

            if line.strip()

        ]

        ignore = [

            "resume",

            "curriculum vitae",

            "cv",

            "email",

            "phone",

            "mobile",

            "address",

            "linkedin",

            "github"

        ]

        for line in lines:

            lower = line.lower()

            if any(word in lower for word in ignore):

                continue

            if any(char.isdigit() for char in line):

                continue

            if len(line.split()) >= 2:

                return line

        return ""

    # ======================================================
    # Skills
    # ======================================================

    def extract_skills(self, text):

        skill_database = [

            "Python",
            "Java",
            "C",
            "C++",
            "C#",
            "SQL",
            "MongoDB",
            "MySQL",
            "PostgreSQL",
            "PyTorch",
            "TensorFlow",
            "Keras",
            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "Data Analysis",
            "Data Science",
            "OpenCV",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Matplotlib",
            "Streamlit",
            "FastAPI",
            "Flask",
            "Django",
            "Docker",
            "Git",
            "GitHub",
            "Linux",
            "AWS",
            "Azure",
            "HTML",
            "CSS",
            "JavaScript"

        ]

        found = []

        lower_text = text.lower()

        for skill in skill_database:

            if skill.lower() in lower_text:

                found.append(skill)

        return sorted(list(set(found)))

    # ======================================================
    # Education
    # ======================================================

    def extract_education(self, text):

        keywords = [

            "bachelor",

            "master",

            "b.tech",

            "m.tech",

            "be",

            "me",

            "b.sc",

            "m.sc",

            "phd",

            "diploma",

            "engineering",

            "university",

            "college",

            "cgpa",

            "percentage"

        ]

        education = []

        for line in text.split("\n"):

            lower = line.lower()

            if any(

                word in lower

                for word in keywords

            ):

                education.append(

                    line.strip()

                )

        return list(dict.fromkeys(education))

    # ======================================================
    # Experience
    # ======================================================

    def extract_experience(self, text):

        patterns = [

            r"\d+\+?\s+years?",

            r"\d+\+?\s+months?",

            r"\d+\s*yrs?",

            r"\d+\s*mos?"

        ]

        experience = []

        for pattern in patterns:

            experience.extend(

                re.findall(

                    pattern,

                    text,

                    re.IGNORECASE

                )

            )

        return list(dict.fromkeys(experience))