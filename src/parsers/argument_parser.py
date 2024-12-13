import argparse

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
    return parser.parse_args()
