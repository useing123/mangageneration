import openai
from ..service import MangaRepository


def generate_title(manga_id: str, manga_genre: str, num_of_chapters: int, repository: MangaRepository) -> None:
    prompt_title = f"Generate a title for a manga in the {manga_genre} genre:"

    response_title = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_title,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    manga_title = response_title.choices[0].text.strip()

    prompt_description = f"Provide a detailed description for the main character of the manga {manga_title} in {manga_genre}: There should be no more than 2 main characters, at least 3, you describe who he is and how he relates to the main characters. Describe everything about the character's appearance, who they are, and what role they play in this manga:"

    response_description = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_description,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    description = response_description.choices[0].text.strip()

    prompt_chapter_title = f"Create a chapter title for the manga '{manga_title}' for the first {num_of_chapters} chapters:"

    response_chapter_title = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_chapter_title,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    chapter_title = response_chapter_title.choices[0].text.strip()

    repository.update_manga(manga_id, {"manga_title": manga_title, "description": description, "chapter_title": chapter_title})
