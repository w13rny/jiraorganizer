from atlassian import Jira
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    jira = Jira(
        url=os.environ.get('JIRA_URL'),
        username=os.environ.get('JIRA_USERNAME'),
        password=os.environ.get('JIRA_TOKEN'),
        cloud=True
    )
