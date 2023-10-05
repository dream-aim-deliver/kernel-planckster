"""
A script to load environment variables from a .env file

Usage from a python script:
    from caps_env import <YOUR_ENVIRONMENT_VARIABLES>


The script depends on the environment variable API_KEY to be defined in an .env file.
You can copy the .env.example file to .env and modify the values as needed or add other environment variables.
"""

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

API_KEY = os.environ.get("API_KEY")
