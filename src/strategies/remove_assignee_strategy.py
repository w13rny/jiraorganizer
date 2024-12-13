from .strategy_interface import Strategy
import logging

class RemoveAssigneeStrategy(Strategy):
    def execute(self, issue: dict, jira_obj):
        issue_status = issue['fields']['status']['name']
        issue_assignee = issue['fields']['assignee']
        if issue_status.lower() == "done" and issue_assignee is not None:
            issue_key = issue['key']
            issue_summary = issue['fields']['summary']
            try:
                jira_obj.assign_issue(issue_key)
                logging.info(f"Issue {issue_key}: {issue_summary} - removed assignee because issue is done")
            except Exception as exc:
                logging.error(f"Error while updating issue {issue_key}: {exc}")
