from fastapi import Depends, HTTPException, status
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from . import router


class MangaGetResponse(AppModel):
    manga_id: str
    genre: str
    chapters_count: int
    manga_chapters_story: list[str]


@router.get("/read/{manga_id}", response_model=MangaGetResponse)
def get_manga(
    manga_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> MangaGetResponse:
    manga_data = svc.repository.get_manga(manga_id)

    if manga_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")

    manga = MangaGetResponse(
        manga_id=str(manga_data["_id"]),
        genre=manga_data["genre"],
        chapters_count=manga_data["chapters_count"],
        manga_chapters_story=manga_data["manga_chapters_story"],
    )

    return manga
