# ==========================================================
# DOCUMENT PROCESSING PIPELINE
# ==========================================================

from models.classifier import DocumentClassifier
from models.ocr import OCR

from extractors.router import DocumentExtractor


class DocumentProcessingPipeline:

    # ------------------------------------------------------
    # Initialize
    # ------------------------------------------------------

    def __init__(self):

        self.classifier = DocumentClassifier()

        self.ocr = OCR()

        self.extractor = DocumentExtractor()

    # ------------------------------------------------------
    # Process Document
    # ------------------------------------------------------

    def process(self, image_path):

        # --------------------------------------------------
        # Step 1 : Classification
        # --------------------------------------------------

        classification = self.classifier.classify(
            image_path
        )

        document_type = classification["prediction"]

        # --------------------------------------------------
        # Step 2 : OCR
        # --------------------------------------------------

        ocr_result = self.ocr.process(
            image_path
        )

        text = ocr_result.get(
            "text",
            ""
        )

        confidence = ocr_result.get(
            "confidence",
            0.0
        )

        # --------------------------------------------------
        # Step 3 : Information Extraction
        # --------------------------------------------------

        extracted_data = self.extractor.extract(

            document_type=document_type,

            text=text

        )

        # --------------------------------------------------
        # Final Result
        # --------------------------------------------------

        return {

            "document_type": document_type,

            "classification": classification,

            "ocr": {

                "text": text,

                "confidence": confidence

            },

            "extracted_data": extracted_data,

            "image_path": image_path

        }

    # ------------------------------------------------------
    # Classification Only
    # ------------------------------------------------------

    def classify_only(self, image_path):

        return self.classifier.classify(
            image_path
        )

    # ------------------------------------------------------
    # OCR Only
    # ------------------------------------------------------

    def ocr_only(self, image_path):

        return self.ocr.process(
            image_path
        )

    # ------------------------------------------------------
    # Extraction Only
    # ------------------------------------------------------

    def extract_only(self, document_type, text):

        return self.extractor.extract(

            document_type=document_type,

            text=text

        )