# ==========================================================
# OCR MODULE
# ==========================================================

import time

import easyocr
import torch


class OCR:

    # ------------------------------------------------------
    # Initialize OCR
    # ------------------------------------------------------

    def __init__(self):

        try:

            self.reader = easyocr.Reader(

                ["en"],

                gpu=torch.cuda.is_available()

            )

        except Exception as e:

            raise RuntimeError(

                f"Failed to initialize EasyOCR:\n{e}"

            )

    # ------------------------------------------------------
    # OCR Processing
    # ------------------------------------------------------

    def process(self, image_path):

        start_time = time.time()

        try:

            result = self.reader.readtext(

                image_path,

                detail=1,

                paragraph=False

            )

        except Exception as e:

            return {

                "text": "",

                "confidence": 0.0,

                "details": [],

                "processing_time": 0.0,

                "error": str(e)

            }

        # --------------------------------------------------
        # Extract Information
        # --------------------------------------------------

        text_lines = []

        details = []

        confidences = []

        for item in result:

            if len(item) < 2:

                continue

            bbox = item[0]

            text = item[1]

            confidence = (

                float(item[2])

                if len(item) > 2

                else 0.0

            )

            text_lines.append(text)

            details.append({

                "bbox": bbox,

                "text": text,

                "confidence": confidence

            })

            confidences.append(confidence)

        # --------------------------------------------------
        # Final Text
        # --------------------------------------------------

        full_text = "\n".join(text_lines)

        # --------------------------------------------------
        # Average Confidence
        # --------------------------------------------------

        average_confidence = (

            sum(confidences) / len(confidences)

            if confidences

            else 0.0

        )

        # --------------------------------------------------
        # Return
        # --------------------------------------------------

        return {

            "text": full_text,

            "confidence": round(

                average_confidence,

                4

            ),

            "details": details,

            "processing_time": round(

                time.time() - start_time,

                4

            )

        }

    # ------------------------------------------------------
    # Helper Functions
    # ------------------------------------------------------

    def extract_text(self, image_path):

        return self.process(

            image_path

        )["text"]

    # ------------------------------------------------------

    def average_confidence(self, image_path):

        return self.process(

            image_path

        )["confidence"]

    # ------------------------------------------------------

    def extract_details(self, image_path):

        return self.process(

            image_path

        )["details"]