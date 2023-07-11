import os

from fastapi import Depends, BackgroundTasks, status
from fastapi.responses import Response

import openai

from app.utils import AppModel

from ..service import Service, get_service, MangaRepository
from . import router


class MangaCreateRequest(AppModel):
    genre: str
    chapters_count: int


class MangaCreateResponse(AppModel):
    manga_id: str


def generate_title(manga_id: str, manga_genre: str, repository: MangaRepository) -> None:
    prompt = f"Generate a title for a manga in the {manga_genre} genre:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_title = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"title": manga_title})


@router.post(
    "/manga", status_code=status.HTTP_201_CREATED, response_model=MangaCreateResponse
)
def create_manga(
    input: MangaCreateRequest,
    background_tasks: BackgroundTasks,
    svc: Service = Depends(get_service),
) -> MangaCreateResponse:
    result = svc.repository.create_manga(input.dict())
    background_tasks.add_task(generate_title, str(result.inserted_id), input.genre, svc.repository)

    return MangaCreateResponse(manga_id=str(result.inserted_id))
