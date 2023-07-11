import openai
from ..service import MangaRepository

#включать выключатель
def fill_manga_info(manga_id: str, manga_genre: str, manga_chapters_cnt: int, repository: MangaRepository) -> None:
    title = generate_title(manga_id, manga_genre, repository)
    generate_chapter_title(manga_id, manga_genre, title, manga_chapters_cnt, repository)
    main_characters = generate_main_characters(manga_id, title, repository)
    fun_characters = generate_funservice_characters(manga_id, title, repository)
    detailed_characters = generate_detailed_characters(manga_id, title, main_characters, fun_characters, repository)
    generate_manga_story(manga_id, manga_genre, title, main_characters, fun_characters, repository)


def generate_title(manga_id: str, manga_genre: str, repository: MangaRepository) -> str:
    prompt = f"Generate a title for a manga in the {manga_genre} genre:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_title = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"title": manga_title})
    return manga_title


def generate_chapter_title(manga_id: str, manga_genre: str, manga_title: str, manga_chapters_cnt: int, repository: MangaRepository) -> None:
    chapters = []
    for index in range(manga_chapters_cnt):
        prompt = f"Generate a title for a chapter #{index + 1}/{manga_chapters_cnt} in manga called '{manga_title}' in {manga_genre} genre:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        chapters.append(response.choices[0].text.strip())
    repository.update_manga(manga_id, {"chapters_title": chapters})


def generate_main_characters(manga_id: str, manga_title: str, repository: MangaRepository) -> str:
    prompt = f"Provide a detailed description for the main characters in the manga {manga_title}:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    main_characters = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"main_characters": main_characters})
    return main_characters


def generate_funservice_characters(manga_id: str, manga_title: str, repository: MangaRepository) -> str:
    prompt = f"Provide a detailed description for the funservice characters in the manga {manga_title}:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    funservice_characters = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"funservice_characters": funservice_characters})
    return funservice_characters


def generate_detailed_characters(manga_id: str, manga_title: str, main_characters: str, funservice_characters: str, repository: MangaRepository) -> str:
    prompt = f"""
    Provide a detailed description for the characters in the manga {manga_title} Description of the characters' appearance in order to draw them:
    {main_characters} {funservice_characters}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    detailed_characters = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"detailed_characters": detailed_characters})
    return detailed_characters


def generate_manga_story(manga_id: str, genre:str, manga_chapters_title: str, manga_title: str, detailed_characters: str, repository: MangaRepository) -> None:
    prompt = f"""
    You are a manga author with 150 years of experience.Create a coherent story that's fun to read, don't limit yourself in anything. Make an interesting ending that makes you want to keep reading. Write an interesting story description for the manga {manga_title} in {genre}, for a chapter called {manga_chapters_title}.
    Character Info:
    {detailed_characters}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_chapters_story = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_chapters_story": manga_chapters_story})


def agent_create_dialogs(manga_id: str, manga_chapters_story: str, repository: MangaRepository) -> None:
    prompt = f"""
    Write Dialogs for this manga chapter story:
    {manga_chapters_story}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_story_dialogs = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_story_dialogs": manga_story_dialogs})


#Вернуться сюда и улучшить промпт
def agent_create_images(manga_id: str, manga_chapters_story: str, repository: MangaRepository) -> None:
    prompt = f"""
    Write detailed description frame by frame for this manga chapter story: 
    {manga_chapters_story}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_story_dialogs = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_story_dialogs": manga_story_dialogs})
