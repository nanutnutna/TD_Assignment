from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(f'{dirname(__file__)}\config.env')
load_dotenv(dotenv_path)
DATABASE_URL=os.environ.get("DATABASE_URL")


def get_database(schema):
    CONNECTION_STRING = DATABASE_URL
    client = MongoClient(CONNECTION_STRING)
    return client[schema]