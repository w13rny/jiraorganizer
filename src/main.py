import argparse
import logging
import os

from atlassian import Jira
from dotenv import load_dotenv

from context import Context
from strategies.add_components_strategy import AddComponentsStrategy
from strategies.add_labels_strategy import AddLabelsStrategy
from strategies.remove_assignee_strategy import RemoveAssigneeStrategy


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('../log.txt', mode='w'),
            logging.StreamHandler()
        ]
    )


def parse_command_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='This simple script helps to organize and manage tasks in Jira.')
    parser.add_argument(
        '--project',
        type=str,
        help='Jira project name'
    )
    parser.add_argument(
        '--delta',
        type=int,
        help='script processes only tasks with limit since the last update (pass value in hours, default=24)',
        default=24
    )
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
        error_message = "Following values not provided in .env file: {}".format(", ".join(env_keys_missing))
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


def get_jira_issues(jql_query: str, jira_obj: Jira) -> list[dict]:
    logging.info(f"Searching issues using following JQL: {jql_query}")
    start_at = 0
    issues = []
    while True:
        request = jira_obj.jql(jql_query, start=start_at, limit=100)
        issues += request['issues']
        start_at = request['startAt']
        max_results = request['maxResults']
        total = request['total']
        if start_at + max_results < total:
            start_at = start_at + max_results
        else:
            break
    logging.info(f"Number of issues found: {len(issues)}")
    return issues


if __name__ == '__main__':
    try:
        configure_logging()
        args = parse_command_line_arguments()
        jira = parse_jira_credentials()
        jql_request = f'project = "{args.project}" AND updated >= -{args.delta}h'
        recently_updated_issues = get_jira_issues(jql_request, jira)

        context = Context(None)
        strategies = [AddComponentsStrategy(), AddLabelsStrategy(), RemoveAssigneeStrategy()]

        for recently_updated_issue in recently_updated_issues:
            for strategy in strategies:
                context.set_strategy(strategy)
                context.execute_strategy(recently_updated_issue, jira)

        logging.info("Issues organization completed successfully.")
    except Exception as e:
        logging.critical(f"Critical error occurred: {e}")
