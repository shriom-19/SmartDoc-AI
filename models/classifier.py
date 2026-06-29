
import time
from pathlib import Path

import torch
import torch.nn as nn

from PIL import Image

from torchvision import transforms
from torchvision.models import resnet50


print("=" * 70)
print("Classifier Loaded From:")
print(__file__)
print("=" * 70)

class DocumentClassifier:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.confidence_threshold = 0.60

        # --------------------------------------------------
        # Image Transform
        # --------------------------------------------------

        self.transform = transforms.Compose([

            transforms.Resize(256),

            transforms.CenterCrop(224),

            transforms.ToTensor(),

            transforms.Normalize(

                mean=[0.485, 0.456, 0.406],

                std=[0.229, 0.224, 0.225]

            )

        ])

        # --------------------------------------------------
        # Default Classes
        # (Will be replaced by checkpoint classes if available)
        # --------------------------------------------------

        self.document_classes = [

            "adhar",

            "advertisement",

            "budget",

            "email",

            "file_folder",

            "form",

            "handwritten",

            "invoice",

            "letter",

            "memo",

            "news_article",

            "pan",

            "presentation",

            "questionnaire",

            "resume",

            "scientific_publication",

            "scientific_report",

            "specification"

        ]

        self.model = self.load_model()

    # ======================================================
    # Load Model
    # ======================================================

    def load_model(self):

        model_path = Path(__file__).parent / "general_document_classifier.pth"

        if not model_path.exists():

            raise FileNotFoundError(

                f"Model not found:\n{model_path}"

            )

        try:

            checkpoint = torch.load(

                model_path,

                map_location=self.device,

                weights_only=False

            )

        except Exception as e:

            raise RuntimeError(

                f"Unable to load model:\n{e}"

            )

        # ------------------------------------------
        # Extract classes and state dict
        # ------------------------------------------

        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:

            # Checkpoint is a wrapped dict: extract parts
            state_dict  = checkpoint["model_state_dict"]

            if "classes" in checkpoint:
                self.document_classes = checkpoint["classes"]

            if "num_classes" in checkpoint:
                num_classes = checkpoint["num_classes"]
            else:
                num_classes = len(self.document_classes)

        elif isinstance(checkpoint, dict) and "state_dict" in checkpoint:

            state_dict = checkpoint["state_dict"]
            num_classes = len(self.document_classes)

        else:

            # Raw state dict
            state_dict  = checkpoint
            num_classes = len(self.document_classes)

        # ------------------------------------------
        # Build model with correct num_classes
        # ------------------------------------------

        model = resnet50(weights=None)

        model.fc = nn.Sequential(

            nn.Dropout(0.5),

            nn.Linear(

                model.fc.in_features,

                num_classes

            )

        )
        print("Loading from:", model_path)
        print("Checkpoint keys:", checkpoint.keys() if isinstance(checkpoint, dict) else "Raw state dict")
        print("Using state_dict type:", type(state_dict))

        model.load_state_dict(state_dict)

        model.to(self.device)

        model.eval()

        return model

    # ======================================================
    # Predict
    # ======================================================

    def predict(self, image_path):

        start_time = time.time()

        try:

            image = Image.open(image_path).convert("RGB")

        except Exception as e:

            return {

                "prediction": "unidentified",

                "class_index": -1,

                "confidence": 0.0,

                "top3_predictions": [],

                "top3_confidences": [],

                "processing_time": 0.0,

                "error": str(e)

            }

        image = self.transform(image)

        image = image.unsqueeze(0).to(self.device)

        with torch.inference_mode():

            output = self.model(image)

            probabilities = torch.softmax(

                output,

                dim=1

            )

            confidence, prediction = torch.max(

                probabilities,

                dim=1

            )

            top3_prob, top3_idx = torch.topk(

                probabilities,

                k=min(

                    3,

                    len(self.document_classes)

                )

            )

        prediction = prediction.item()

        confidence = confidence.item()

        if confidence < self.confidence_threshold:

            document_type = "unidentified"

        else:

            document_type = self.document_classes[prediction]

        return {

            "prediction": document_type,

            "class_index": prediction,

            "confidence": round(confidence, 4),

            "top3_predictions": [

                self.document_classes[i]

                for i in top3_idx[0].cpu().tolist()

            ],

            "top3_confidences": [

                round(float(i), 4)

                for i in top3_prob[0].cpu().tolist()

            ],

            "processing_time": round(

                time.time() - start_time,

                4

            )

        }

    # ======================================================
    # Classify
    # ======================================================

    def classify(self, image_path):

        return self.predict(

            image_path

        )