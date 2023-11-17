from atlassian import Jira
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    jira = Jira(
        url=os.environ.get('ATLASSIAN_URL'),
        username=os.environ.get('ATLASSIAN_USERNAME'),
        password=os.environ.get('ATLASSIAN_API_TOKEN'),
        cloud=True
    )
