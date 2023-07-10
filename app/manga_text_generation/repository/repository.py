from fastapi import Depends
from fastapi.param_functions import Query
from app.utils import AppModel

from ..service import Service, get_service
from ..repository import TextRepository
from . import router


class GenreInput(AppModel):
    genre: str = Query(..., description="Genre of the titles")
    number_of_titles: int = Query(..., gt=0, description="Number of titles to retrieve")
