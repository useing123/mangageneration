from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult
from bson.objectid import ObjectId

from ..utils.security import hash_password


class MangaRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_manga(self, input_data: dict) -> InsertOneResult:
        payload = {
            "genre": input_data["genre"],
            "chapters_count": input_data["chapters_count"],
        }

        return self.database["manga_text"].insert_one(payload)

    def update_manga(self, manga_id: str, update_data: dict) -> UpdateResult:
        return self.database["manga_text"].update_one(
            {"_id": ObjectId(manga_id)}, {"$set": update_data}
        )
