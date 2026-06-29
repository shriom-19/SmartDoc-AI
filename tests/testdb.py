import sys
import os

# Add the project root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongodb import MongoDB

# ==========================================================
# TEST MONGODB CONNECTION
# ==========================================================

def main():

    mongo = MongoDB()

    if mongo.test_connection():

        print("[SUCCESS] MongoDB Connected Successfully!")

        collection = mongo.get_collection()

        print(f"Database   : {mongo.database_name}")
        print(f"Collection : {mongo.collection_name}")

        total = collection.count_documents({})

        print(f"Documents  : {total}")

    else:

        print("[FAILED] Failed to connect to MongoDB.")

    mongo.close()


if __name__ == "__main__":

    main()
