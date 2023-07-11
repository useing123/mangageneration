from app.config import database


from .repository.repository import MangaRepository


class Service:
    def __init__(
        self,
        repository: MangaRepository,
    ):
        self.repository = repository


def get_service():
    repository = MangaRepository(database)
    svc = Service(repository)
    return svc