import argparse
import os

from atlassian import Jira
from dotenv import load_dotenv


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='This simple script helps to organize and manage tasks in Jira.')
    parser.add_argument(
        '--project',
        type=str,
        help='Jira project name')
    parser.add_argument(
        '--delta',
        type=int,
        help='script processes only tasks with limit since the last update (pass value in hours, default=24)',
        default=24)
    arguments = parser.parse_args()
    return arguments


def check_environment_variables():
    load_dotenv()
    env_keys = ['JIRA_URL', 'JIRA_USERNAME', 'JIRA_API_TOKEN']
    env_keys_missing = []
    for env_key in env_keys:
        if os.environ.get(env_key) is None:
            env_keys_missing.append(env_key)
    if env_keys_missing:
        error_message = "Following values not provided in .env file: "
        error_message += ", ".join(env_keys_missing)
        raise Exception(error_message)


def parse_jira_credentials() -> Jira:
    check_environment_variables()
    jira_obj = Jira(
        url=os.environ.get('JIRA_URL'),
        username=os.environ.get('JIRA_USERNAME'),
        password=os.environ.get('JIRA_API_TOKEN'),
        cloud=True
    )
    return jira_obj


if __name__ == '__main__':
    try:
        args = parse_arguments()
        jira = parse_jira_credentials()
        jql_request = f'project = "{args.project}" AND updated >= -{args.delta}h'
        issues = jira.jql(jql_request)
        print(issues)
    except Exception as e:
        print(f"Error occurred: {e}")
