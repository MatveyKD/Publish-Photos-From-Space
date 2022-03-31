from pathlib import Path

import requests


def fetch_spacex_images(path):
    Path(path).mkdir(parents=True, exist_ok=True)

    flight_number = 100
    url = f"https://api.spacexdata.com/v3/launches/{flight_number}"
    response = requests.get(url)
    response.raise_for_status()
    images_links = response.json()["links"]["flickr_images"]
    for index, image_link in enumerate(images_links):
        response = requests.get(image_link)
        response.raise_for_status()
        with open(f"{path}spacex{index}.jpg", 'wb') as file:
            file.write(response.content)
