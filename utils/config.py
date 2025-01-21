import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    token = os.getenv("TOKEN", "")
    cloud_folder_name = os.getenv("CLOUD_FOLDER_NAME", "my_cloud_folder")
    local_folder_name = os.getenv("LOCAL_FOLDER_NAME", "my_local_folder")
    periodicity = float(os.getenv("PERIODICITY", "3"))


config = Config()
