import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN = os.getenv("TOKEN")
    CLOUD_FOLDER_NAME = os.getenv("CLOUD_FOLDER_NAME")


config = Config()
