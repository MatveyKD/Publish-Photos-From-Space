import os
from dotenv import dotenv_values
import time
from pathlib import Path

import telegram

import fetch_nasa_images
from fetch_spacex_images import fetch_spacex_images


if __name__ == "__main__":
    bot = telegram.Bot(dotenv_values(".env")["BOT_TOKEN"])
    api_key = dotenv_values(".env")["API_KEY"]
    dirs = [
        "spacex",
        "nasa",
        "epic"
    ]
    for directory in dirs:
        Path(f"images/{directory}").mkdir(parents=True, exist_ok=True)
    while True:
        fetch_nasa_images.fetch_nasa_epic_images("images/epic/", api_key)
        fetch_spacex_images("images/spacex/")
        fetch_nasa_images.fetch_nasa_images("images/nasa/", api_key)

        for dirpath, dirnames, filenames in os.walk("images"):
            for filename in filenames:
                image_path = os.path.join(dirpath, filename)
                with open(image_path, 'rb') as image:
                    bot.send_document(
                        chat_id=dotenv_values(".env")["CHAT_ID"],
                        document=image
                    )
                time.sleep(10)

        time.sleep(int(dotenv_values(".env")["SLEEP_VALUE"]))
