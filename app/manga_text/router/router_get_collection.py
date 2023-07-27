from fastapi import Depends, HTTPException, status
from app.utils import AppModel
from ..service import Service, get_service
from . import router

from typing import List

from typing import Optional

class MangaCollectionResponse(AppModel):
    manga_id: str
    genre: str
    title: Optional[str] 
    main_characters: Optional[str] 

@router.get("/read/all", response_model=List[MangaCollectionResponse])
def get_all_mangas(
    svc: Service = Depends(get_service),
) -> List[MangaCollectionResponse]:
    mangas_data = svc.repository.get_all_mangas()

    mangas = [MangaCollectionResponse(
        manga_id=str(manga["_id"]),
        genre=manga.get("genre"),
        title=manga.get("title"),
        main_characters=manga.get("main_characters")
    ) for manga in mangas_data]

    return mangas

