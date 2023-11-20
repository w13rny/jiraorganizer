import argparse
import logging
import os

from atlassian import Jira
from dotenv import load_dotenv

COMPONENTS = [
    ("[B]", "Backend"),
    ("[F]", "Frontend"),
]

LABELS = [
    ("[D]", "designer"),
]


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('log.txt', mode='w'),
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


def strategy_add_components(issue: dict, jira_obj: Jira):
    issue_summary = issue['fields']['summary']
    issue_current_components = []
    if issue['fields']['components']:
        for issue_component in issue['fields']['components']:
            issue_current_components.append(issue_component['name'])
    for COMPONENT in COMPONENTS:
        if COMPONENT[0] in issue_summary and COMPONENT[1] not in issue_current_components:
            issue_key = issue['key']
            fields = {"components": [{"add": {"name": COMPONENT[1]}}]}
            try:
                jira_obj.edit_issue(issue_key, fields, notify_users=False)
                logging.info(f"Issue {issue_key}: {issue_summary} - added component: {COMPONENT[1]}")
            except Exception as exc:
                logging.error(f"Error while updating issue {issue_key}: {exc}")


def strategy_add_labels(issue: dict, jira_obj: Jira):
    issue_summary = issue['fields']['summary']
    issue_current_labels = []
    if issue['fields']['labels']:
        for issue_label in issue['fields']['labels']:
            issue_current_labels.append(issue_label)
    for LABEL in LABELS:
        if LABEL[0] in issue_summary and LABEL[1] not in issue_current_labels:
            issue_key = issue['key']
            fields = {"labels": [{"add": LABEL[1]}]}
            try:
                jira_obj.edit_issue(issue_key, fields, notify_users=False)
                logging.info(f"Issue {issue_key}: {issue_summary} - added label: {LABEL[1]}")
            except Exception as exc:
                logging.error(f"Error while updating issue {issue_key}: {exc}")


if __name__ == '__main__':
    try:
        configure_logging()
        args = parse_command_line_arguments()
        jira = parse_jira_credentials()
        jql_request = f'project = "{args.project}" AND updated >= -{args.delta}h'
        recently_updated_issues = get_jira_issues(jql_request, jira)
        for recently_updated_issue in recently_updated_issues:
            strategy_add_components(recently_updated_issue, jira)
            strategy_add_labels(recently_updated_issue, jira)
        logging.info(f"Issues organization completed successfully.")
    except Exception as e:
        logging.critical(f"Critical error occurred: {e}")
