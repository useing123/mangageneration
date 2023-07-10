from fastapi import Depends
from fastapi.param_functions import Query
from app.utils import AppModel

from ..service import Service, get_service
from . import router

class GenreInput(AppModel):
    genre: str = Query(..., description="Genre of the titles")
    number_of_titles: int = Query(..., gt=0, description="Number of titles to retrieve")

@router.get("/titles")
def get_titles_by_genre(
    input: GenreInput,
    svc: Service = Depends(get_service),
):
    genre = input.genre
    number_of_titles = input.number_of_titles

    # Call your service function to retrieve titles based on genre and number_of_titles
    titles = svc.get_titles_by_genre(genre, number_of_titles)

    return {"titles": titles}
