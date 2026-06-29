from extractors.common import CommonExtractor

from extractors.invoice import InvoiceExtractor
from extractors.resume import ResumeExtractor
from extractors.adhar import AadhaarExtractor
from extractors.pan import PANExtractor
from extractors.form import FormExtractor


class DocumentExtractor:

    def __init__(self):

        self.common = CommonExtractor()

        self.extractors = {

            # Specialized Extractors

            "invoice": InvoiceExtractor(),

            "resume": ResumeExtractor(),

            "adhar": AadhaarExtractor(),

            "pan": PANExtractor(),

            "form": FormExtractor()

        }

    # =====================================================
    # Main Router
    # =====================================================

    def extract(self, document_type: str, text: str):

        document_type = document_type.lower().strip()

        extractor = self.extractors.get(

            document_type,

            self.common

        )

        if extractor == self.common:

            return self.common.extract(

                text=text,

                document_type=document_type

            )

        return extractor.extract(

            text

        )

    # =====================================================
    # Register New Extractor
    # =====================================================

    def register(self, document_type: str, extractor):

        self.extractors[

            document_type.lower().strip()

        ] = extractor

    # =====================================================
    # Supported Document Types
    # =====================================================

    def supported_documents(self):

        return sorted(

            self.extractors.keys()

        )