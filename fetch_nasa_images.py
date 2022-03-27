import requests
import os
from urllib.parse import urlparse


def load_image(url, path, payload=None):    
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)

def fetch_nasa_images(path, api_key):
    url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "api_key": api_key,
        "count": 50
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for index, image_link in enumerate(response.json()):
        if image_link["media_type"] != "video":
            response = requests.get(image_link["url"])
            response.raise_for_status()
            with open(path + "nasa" + str(index) + get_file_type(image_link["url"]), "wb") as file:
                file.write(response.content)

def get_file_type(url):
    return os.path.splitext(urlparse(url).path)[1]

def fetch_nasa_epic_images(path, api_key):
    url = "https://api.nasa.gov/EPIC/api/natural"
    payload = {
        "api_key": api_key,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    epic_launches = response.json()

    for index, launch in enumerate(epic_launches):
        image_name = launch["image"]
        image_date = image_name[8:12:]+"/"+image_name[12:14:]+"/"+image_name[14:16:]
        url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png"
        payload = {
            "api_key": api_key,
        }

        load_image(url, path + f"nasa_epic{index}.png", payload)
