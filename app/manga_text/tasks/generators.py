import os
import openai
import replicate
import time
from ..service import MangaRepository
import replicate
import requests

import base64
import re

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
IMGUR_CLIENT_SECRET = os.getenv("IMGUR_CLIENT_SECRET")


#включать выключатель
def fill_manga_info(manga_id: str, manga_genre: str, prompt:str, manga_chapters_cnt: int, repository: MangaRepository) -> None:
    title = generate_title(manga_id, manga_genre, prompt, repository)
    time.sleep(17)
    main_characters = generate_main_characters(manga_id, title, manga_genre, repository)
    time.sleep(17)
    fun_characters = generate_funservice_characters(manga_id, title, manga_genre, repository)
    time.sleep(17)
    detailed_characters = generate_detailed_characters(manga_id, title, main_characters, fun_characters, repository)
    time.sleep(37)
    chapter_title = generate_chapter_title(manga_id, manga_genre, title, manga_chapters_cnt, repository)
    time.sleep(17)
    manga_story = generate_manga_story(manga_id, manga_genre, title, chapter_title, main_characters, fun_characters, repository)
    time.sleep(17)
    manga_frames_description = agent_create_frames_description(manga_id, manga_story, repository)
    time.sleep(17)
    manga_dialogs = agent_create_dialogs(manga_id, manga_frames_description, repository)
    time.sleep(17)
    prompt_image_description = agent_create_images_description(manga_id, manga_frames_description, detailed_characters, repository)
    # time.sleep(17)
    generate_image(manga_id, prompt_image_description, repository)


def generate_title(manga_id: str, manga_genre: str, prompt:str, repository: MangaRepository) -> str:
    prompt = f"""
    Generate a title for a manga in the {manga_genre} genre, give output without quotation marks:
    Keep this {prompt} in mind 
    In 2-5 words
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=1,
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
            max_tokens=125,
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
    Limit your text to no more than 1200 tokens
    Give output like this "Name" - "text" with forewords
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
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
    Limit your text to no more than 900 tokens
    Give output like this "Name" - "text" with forewords
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1200,
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
    Limit your text to no more than 900 tokens
    Give output like this "Name" - "description" with forewords
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    detailed_characters = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"detailed_characters": detailed_characters})
    return detailed_characters


def generate_manga_story(manga_id: str, genre:str, manga_chapters_title: str, manga_title: str, main_characters:str, funservice_characters:str, repository: MangaRepository) -> str:
    """
    Parameters:
    manga_id: str
    genre: str
    manga_chapters_title: str
    manga_title: str
    main_characters: str
    funservice_characters: str
    repository: MangaRepository
    """

    prompt = f"""
    You are a manga author with 30 years of experience. Create a coherent story that's fun to read, don't limit yourself in anything. Make an interesting ending that makes you want to keep reading. Write an interesting story description for the manga {manga_title} in {genre}, for a chapter called {manga_chapters_title}.
    Avoid mentioning "funservice" in the story, just write names of the characters.
    Character Info:
    {main_characters}
    {funservice_characters}
    put the story at 3,800 tokens.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a manga writer with 30 years of experience. put the story at 3,800 tokens."},
            {"role": "user", "content": prompt}
        ]
    )
    
    manga_chapters_story = response['choices'][0]['message']['content'].strip()
    repository.update_manga(manga_id, {"manga_chapters_story": manga_chapters_story})
    return manga_chapters_story




#Описываем 15 кадров манги
def agent_create_frames_description(manga_id: str, manga_chapters_story: str, repository: MangaRepository) -> str:
    prompt = f"""
    Make it 15 frames for this manga what happens in 15 frames
    give output like this:
    avoid meaning "funservice" in the frames just write names of the characters
    Design text like this:
    Frame №1: "Something happens"
    {manga_chapters_story}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4096,
        n=1,
        stop=None,
        temperature=0.1,
    )
    manga_frames_description = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_frames_description": manga_frames_description})
    return manga_frames_description


#Эта штука извлекает диалоги из фреймов
def agent_create_dialogs(manga_id: str, manga_frames_description: str, repository: MangaRepository) -> str:
    prompt = f"""
    Write what happens(dialogs, sound effects, etc.) for this manga frames:
    give output like this:
    Frame №1: "What happens in this frame"
    {manga_frames_description}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.1,
    )
    manga_story_dialogs = response.choices[0].text.strip()
    repository.update_manga(manga_id, {"manga_story_dialogs": manga_story_dialogs})
    return manga_story_dialogs

#Эта штука извлекает описание сцены из фреймов надо переписать нормальной пока что это затычка нужно будет зайти в https://huggingface.co/datasets/Gustavosta/Stable-Diffusion-Prompts/viewer/Gustavosta--Stable-Diffusion-Prompts/test и взять от туда
def agent_create_images_description(manga_id: str, manga_frames_description: str, detailed_characters: str, repository: MangaRepository) -> str:
    """
    Parameters:
    manga_id (str): The ID of the manga.
    detailed_characters (str): The detailed description of the characters.
    manga_frames_description (str): The frames description of the manga, what happens on the frames.
    repository (MangaRepository): An instance of the MangaRepository class.
    Returns:
    str: Prompts for painting images using Stable Diffusion.
    """
    prompt = f"I need to upgrade the following prompt for generating an image using Stable Diffusion: '{detailed_characters}' '{manga_frames_description}'. Please provide a detailed and specific version of this prompt."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are manga painter with 150 years experience. You need to draw 15 frames for this manga."},
            {"role": "user", "content": prompt}
        ]
    )
    
    manga_images_description = response['choices'][0]['message']['content'].strip()
    repository.update_manga(manga_id, {"manga_images_description": manga_images_description})
    return manga_images_description


# Тут должна быть штука которая ИИ модель заходит в ембединг и пишет text2stable diffusion prompt
# def generate_text_to_stable_diffusion_prompt(manga_frames_description: str) -> str:
#     # Construct a prompt for text-to-stable-diffusion
#     prompt = f"Input: {manga_frames_descripti let a: on}\nOutput:"

#     # ... Additional logic to customize the prompt as needed ...

#     return prompt

# def generate_image(manga_id: str, manga_images_description: str, repository: MangaRepository): 
#     os.environ["REPLICATE_API_TOKEN"] = replicate_api_key

#     # Split the input text into frames
#     frames = re.split(r'Frame №\d+: ', input_text)[1:]

#     imgur_links = []

#     for frame in frames:
#         # Call the Replicate API to generate an image
#         model_version = "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061"
#         inputs = {"prompt": frame}
#         output_urls = replicate.run(model_version, input=inputs)

#         # The output_urls is a list of URLs, we'll just use the first one
#         image_url = output_urls[0]

#         # Download the image
#         image_response = requests.get(image_url)

#         # Convert the image to base64
#         image_base64 = base64.b64encode(image_response.content).decode()

#         # Call the Imgur API to upload the image
#         headers = {
#             "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
#         }
#         data = {
#             "image": image_base64,
#             "type": "base64"
#         }
#         response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)

#         # Add the Imgur link to the list
#         imgur_links.append(response.json()["data"]["link"])

#     # Return the Imgur links
#     return {"imgur_links": imgur_links}


def generate_image(manga_id: str, manga_images_description: str, repository: MangaRepository): 
    replicate_api_token = REPLICATE_API_TOKEN
    imgur_client_id_value = IMGUR_CLIENT_ID

    frames = re.split(r'Frame №\d+: ', manga_images_description)[1:]

    imgur_links = []

    for frame in frames:
        # Call the Replicate API to generate an image
        model_version = "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061"
        inputs = {"prompt": frame}

        # We need to set the token environment variable for the replicate.run function
        os.environ['REPLICATE_API_TOKEN'] = replicate_api_token

        outputs = replicate.run(model_version, input=inputs)

        # The outputs contains a list of URLs, we'll just use the first one
        image_url = outputs[0]

        # Download the image
        image_response = requests.get(image_url)

        # Convert the image to base64
        image_base64 = base64.b64encode(image_response.content).decode()

        # Call the Imgur API to upload the image
        headers = {
            "Authorization": f"Client-ID {imgur_client_id_value}"
        }
        data = {
            "image": image_base64,
            "type": "base64"
        }
        response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)

        # Add the Imgur link to the list
        imgur_links.append(response.json()["data"]["link"])

    # Update manga information with the Imgur links in the repository
    repository.update_manga(manga_id, {"imgur_links": imgur_links})

    # Return the Imgur links
    return {"imgur_links": imgur_links}