import os
from dotenv import load_dotenv

def check_environment_variables():
    load_dotenv()
    env_keys = ['JIRA_URL', 'JIRA_USERNAME', 'JIRA_API_TOKEN']
    env_keys_missing = [env_key for env_key in env_keys if os.environ.get(env_key) is None]
    if env_keys_missing:
        error_message = "Following values not provided in .env file: {}".format(", ".join(env_keys_missing))
        raise Exception(error_message)
