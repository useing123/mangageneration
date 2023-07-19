from fastapi import Depends, BackgroundTasks, status

from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from ..tasks.generators import fill_manga_info
from . import router


class MangaCreateRequest(AppModel):
    genre: str
    chapters_count: int


class MangaCreateResponse(AppModel):
    manga_id: str


@router.post(
    "/generate", status_code=status.HTTP_201_CREATED, response_model=MangaCreateResponse
)
def create_manga(
    input: MangaCreateRequest,
    background_tasks: BackgroundTasks,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> MangaCreateResponse:
    result = svc.repository.create_manga(input.dict(), jwt_data.user_id)

    manga_id = str(result.inserted_id)
    manga_genre = input.genre
    num_of_chapters = input.chapters_count

    background_tasks.add_task(
        fill_manga_info,
        manga_id,
        manga_genre,
        num_of_chapters,
        svc.repository
    )

    return MangaCreateResponse(manga_id=manga_id)
