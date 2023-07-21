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
    user_id: str
    title: str
    chapters_title: list[str]
    main_characters: str
    funservice_characters: str
    detailed_characters: str
    manga_chapters_story: str
    manga_frames_description: str
    manga_story_dialogs: str
    manga_images_description: str

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
        user_id=manga_data.get("user_id", ""),
        title=manga_data.get("title", ""),
        chapters_title=manga_data.get("chapters_title", []),
        main_characters=manga_data.get("main_characters", ""),
        funservice_characters=manga_data.get("funservice_characters", ""),
        detailed_characters=manga_data.get("detailed_characters", ""),
        manga_chapters_story=manga_data.get("manga_chapters_story", ""),
        manga_frames_description=manga_data.get("manga_frames_description", ""),
        manga_story_dialogs=manga_data.get("manga_story_dialogs", ""),
        manga_images_description=manga_data.get("manga_images_description", "")
    )

    return manga
