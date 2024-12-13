import os
from atlassian import Jira
from .env_parser import check_environment_variables

def parse_jira_credentials() -> Jira:
    check_environment_variables()
    return Jira(
        url=os.environ.get('JIRA_URL'),
        username=os.environ.get('JIRA_USERNAME'),
        password=os.environ.get('JIRA_API_TOKEN'),
        cloud=True
    )
