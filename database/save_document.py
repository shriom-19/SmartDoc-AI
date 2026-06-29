from datetime import datetime
from bson import ObjectId

from database.mongodb import MongoDB


class DocumentDatabase:

    def __init__(self):

        self.collection = MongoDB().get_collection()

    # =====================================================
    # Helper
    # =====================================================

    def _serialize(self, document):

        if document:

            document["_id"] = str(document["_id"])

        return document

    # =====================================================
    # Save Document
    # =====================================================

    def save_document(self, data):

        document = data.copy()

        now = datetime.utcnow()

        document["created_at"] = now
        document["updated_at"] = now

        result = self.collection.insert_one(document)

        return str(result.inserted_id)

    # =====================================================
    # Get All Documents
    # =====================================================

    def get_all_documents(self):

        documents = list(

            self.collection.find().sort(
                "created_at",
                -1
            )

        )

        return [

            self._serialize(doc)

            for doc in documents

        ]

    # =====================================================
    # Get Document
    # =====================================================

    def get_document(self, document_id):

        try:
            document = self.collection.find_one(
                {"_id": ObjectId(document_id)}
            )
        except Exception:
            return None

        return self._serialize(document)

    # =====================================================
    # Update Document
    # =====================================================

    def update_document(self, document_id, updated_data):

        updated_data["updated_at"] = datetime.utcnow()

        try:
            result = self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": updated_data}
            )
            return result.modified_count
        except Exception:
            return 0

    # =====================================================
    # Delete Document
    # =====================================================

    def delete_document(self, document_id):

        try:
            result = self.collection.delete_one(
                {"_id": ObjectId(document_id)}
            )
            return result.deleted_count
        except Exception:
            return 0

    # =====================================================
    # Search by Type
    # =====================================================

    def search_by_type(self, document_type):

        documents = list(

            self.collection.find(

                {

                    "document_type": {

                        "$regex": f"^{document_type}$",

                        "$options": "i"

                    }

                }

            )

        )

        return [

            self._serialize(doc)

            for doc in documents

        ]

    # =====================================================
    # Search by Filename
    # =====================================================

    def search_by_filename(self, filename):

        documents = list(

            self.collection.find(

                {

                    "filename": {

                        "$regex": filename,

                        "$options": "i"

                    }

                }

            )

        )

        return [

            self._serialize(doc)

            for doc in documents

        ]

    # =====================================================
    # Search by Vendor
    # =====================================================

    def search_by_vendor(self, vendor):

        documents = list(

            self.collection.find(

                {

                    "extracted_data.vendor": {

                        "$regex": vendor,

                        "$options": "i"

                    }

                }

            )

        )

        return [

            self._serialize(doc)

            for doc in documents

        ]

    # =====================================================
    # Total Documents
    # =====================================================

    def total_documents(self):

        return self.collection.count_documents({})

    # =====================================================
    # Count by Type
    # =====================================================

    def count_by_type(self, document_type):

        return self.collection.count_documents(

            {

                "document_type": document_type

            }

        )

    # =====================================================
    # Recent Documents
    # =====================================================

    def recent_documents(self, limit=10):

        documents = list(

            self.collection.find()

            .sort(

                "created_at",

                -1

            )

            .limit(limit)

        )

        return [

            self._serialize(doc)

            for doc in documents

        ]

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "total_documents": self.total_documents(),

            "recent_documents": len(

                self.recent_documents()

            )

        }

    # =====================================================
    # Delete All
    # =====================================================

    def delete_all_documents(self):

        result = self.collection.delete_many({})

        return result.deleted_count