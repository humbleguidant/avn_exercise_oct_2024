# This is the config file for loading the .env variables and
# creating the connection to the database

import os
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient

# load the env vars.
env_path = Path('../.env')
load_dotenv(env_path)

# create database connection
def get_db():
    client = MongoClient('mongodb://' + os.environ.get('MONGODB_USER') +
                         ':' + os.environ.get('MONGODB_PASS') + '@' + os.environ.get('MONGODB_HOST') +
                         ':' + os.environ.get('MONGODB_PORT') + '/')
    db = client[os.environ.get('MONGODB_DATABASE')]
    return db

# get secret key for creating sessions
def get_secret_key():
    return str(os.environ.get('SECRET_SESSION_KEY'))