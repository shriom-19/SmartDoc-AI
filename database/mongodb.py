import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


class MongoDB:

    def __init__(self):

        self.connection_string  = os.getenv("MONGODB_URI")
        self.database_name      = os.getenv("DATABASE_NAME", "DocumentAI")
        self.collection_name    = os.getenv("COLLECTION_NAME", "documents")

        if not self.connection_string:
            raise ValueError(
                "MONGODB_URI not found in .env file. "
                "Create a .env file with: MONGODB_URI=<your_connection_string>"
            )

        import certifi
        self.client = MongoClient(
            self.connection_string,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=10000,
            tlsCAFile=certifi.where()
        )

        self.db         = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    # ======================================================
    # Collection
    # ======================================================

    def get_collection(self):
        return self.collection

    # ======================================================
    # Test Connection
    # ======================================================

    def test_connection(self):
        try:
            self.client.admin.command("ping")
            return True
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            return False

    # ======================================================
    # Connection Status
    # ======================================================

    def is_connected(self):
        return self.test_connection()

    # ======================================================
    # Close Connection
    # ======================================================

    def close(self):
        if self.client:
            self.client.close()