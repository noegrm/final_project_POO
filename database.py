import json
import os

class DatabaseManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(BASE_DIR, "database.json")

    @staticmethod
    def load():
        if not os.path.exists(DatabaseManager.FILE_PATH):
            return {"users": [], "accounts": [], "transactions": []}

        with open(DatabaseManager.FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save(data):
        with open(DatabaseManager.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
