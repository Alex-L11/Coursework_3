import os

from dotenv import load_dotenv

load_dotenv()

db_config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}


COUNTRIES = ["Canada", "Spain", "France", "Japan", "Poland"]
