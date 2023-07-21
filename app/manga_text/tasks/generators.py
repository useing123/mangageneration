import openai
import time
from ..service import MangaRepository

#включать выключатель
def fill_manga_info(manga_id: str, manga_genre: str, manga_chapters_cnt: int, repository: MangaRepository) -> None:
    title = generate_title(manga_id, manga_genre, repository)
    time.sleep(20)
    generate_chapter_title(manga_id, manga_genre, title, manga_chapters_cnt, repository)
    time.sleep(20)
    main_characters = generate_main_characters(manga_id, title, manga_genre, repository)
    time.sleep(20)
    fun_characters = generate_funservice_characters(manga_id, title, manga_genre, repository)
    time.sleep(20)
    detailed_characters = generate_detailed_characters(manga_id, title, main_characters, fun_characters, repository)
    time.sleep(20)
    manga_story = generate_manga_story(manga_id, manga_genre, title, main_characters, fun_characters, repository)
    time.sleep(20)
    manga_frames_description = agent_create_frames_description(manga_id, manga_story, repository)
    time.sleep(20)
    manga_dialogs = agent_create_dialogs(manga_id, manga_story, repository)
    time.sleep(20)
    prompt_image_description = agent_create_images_description(manga_id, manga_frames_description, repository)




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


def generate_main_characters(manga_id: str, manga_title: str, genre: str, repository: MangaRepository) -> str:
    prompt = f"""
    Provide a detailed description for the main characters in the manga {manga_title}:
    Study the features of this genre: {genre} and write detailed main character descriptions
    """
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


def generate_funservice_characters(manga_id: str, manga_title: str, genre: str, repository: MangaRepository) -> str:
    prompt = f"""
    Provide a detailed description for the funservice characters in the manga {manga_title}:
    Study the features of this genre: {genre} and write detailed main character descriptions
    """
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


def generate_manga_story(manga_id: str, genre:str, manga_chapters_title: str, manga_title: str, detailed_characters: str, repository: MangaRepository) -> str:
    prompt = f"""
    You are a manga author with 150 years of experience.Create a coherent story that's fun to read, don't limit yourself in anything. Make an interesting ending that makes you want to keep reading. Write an interesting story description for the manga {manga_title} in {genre}, for a chapter called {manga_chapters_title}.
    Avoid meaning "funservice" in the story just write names of the characters
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
    return manga_chapters_story


def agent_create_frames_description(manga_id: str, manga_chapters_story: str, repository: MangaRepository) -> str:
    prompt = f"""
    Make it 7 frames for this manga what happens in 7 frames
    give output like this:
    avoid meaning "funservice" in the frames just write names of the characters
    Frame №1: "Something happens"
    {manga_chapters_story}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_frames_description = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_frames_description": manga_frames_description})
    return manga_frames_description


#Эта штука извлекает диалоги из текста который сгенерировался
def agent_create_dialogs(manga_id: str, manga_frames_description: str, repository: MangaRepository) -> str:
    prompt = f"""
    Write Dialogs for this manga chapter story:
    give output like this:
    Frame №1: "Dialogs"
    {manga_frames_description}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manga_story_dialogs = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_story_dialogs": manga_story_dialogs})
    return manga_story_dialogs

#Эта штука извлекает описание сцены из текста который сгенерировался
def agent_create_images_description(manga_id: str, manga_frames_description: str, repository: MangaRepository) -> str:
    """
    Upgrade a user prompt for Stable Diffusion image generation using GPT-3.5-turbo.

    Parameters:
    manga_id (str): The ID of the manga.
    manga_frames_description (str): The user's original prompt for generating images.
    repository (MangaRepository): An instance of the MangaRepository class.

    Returns:
    None
    """
    prompt = f"I need to upgrade the following prompt for generating an image using Stable Diffusion: '{manga_frames_description}'. Please provide a detailed and specific version of this prompt."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    manga_images_description = response['choices'][0]['message']['content'].strip()
    repository.update_manga(manga_id, {"manga_images_description": manga_images_description})
    return manga_images_description


# Тут должна быть штука которая ИИ модель заходит в ембединг и пишет text2stable diffusion prompt
def generate_text_to_stable_diffusion_prompt(manga_chapters_story: str) -> str:
    # Construct a prompt for text-to-stable-diffusion
    prompt = f"Input: {manga_chapters_story}\nOutput:"

    # ... Additional logic to customize the prompt as needed ...

    return prompt



#Тут должна быть штука которая берет текст и генерирует картинку через репликат и в отдельную колекцию сохраняет урлы

#https://replicate.com/docs/get-started/python