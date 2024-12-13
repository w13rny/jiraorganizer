import logging

from context import Context
from parsers.argument_parser import parse_command_line_arguments
from parsers.jira_parser import parse_jira_credentials
from strategies.add_components_strategy import AddComponentsStrategy
from strategies.add_labels_strategy import AddLabelsStrategy
from strategies.remove_assignee_strategy import RemoveAssigneeStrategy


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('log.txt', mode='w'),
            logging.StreamHandler()
        ]
    )

def get_jira_issues(jql_query: str, jira_obj) -> list[dict]:
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

        for issue in recently_updated_issues:
            for strategy in strategies:
                context.set_strategy(strategy)
                context.execute_strategy(issue, jira)

        logging.info("Issues organization completed successfully.")
    except Exception as e:
        logging.critical(f"Critical error occurred: {e}")
