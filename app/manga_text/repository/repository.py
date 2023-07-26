from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult
from bson.objectid import ObjectId
from typing import Optional

from ..utils.security import hash_password


class MangaRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_manga(self, input_data: dict, user_id: str) -> InsertOneResult:
        payload = {
            "genre": input_data["genre"],
            "chapters_count": input_data["chapters_count"],
            "user_id": user_id,
        }

        return self.database["mangas"].insert_one(payload)

    def update_manga(self, manga_id: str, update_data: dict) -> UpdateResult:
        return self.database["mangas"].update_one(
            {"_id": ObjectId(manga_id)}, {"$set": update_data}
        )

    def create_chapter(self, input_data: dict, manga_id: str) -> InsertOneResult:
        payload = {
            "tite": input_data["title"],
            "chapters_count": input_data["chapters_count"],
            "manga_id": manga_id,
        }

        return self.database["manga_chapters"].insert_one(payload)

    def get_manga_chapters_story(self, manga_id: str) -> Optional[list[str]]:
        manga_data = self.database["mangas"].find_one({"_id": ObjectId(manga_id)})
        if manga_data:
            return manga_data.get("manga_chapters_story")
        else:
            return None

    def get_manga(self, manga_id: str) -> Optional[dict]:
        return self.database["mangas"].find_one({"_id": ObjectId(manga_id)})
    
    