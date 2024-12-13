from .strategy_interface import Strategy
import logging

class AddLabelsStrategy(Strategy):
    LABELS = [
        ("[D]", "designer"),
    ]

    def execute(self, issue: dict, jira_obj):
        issue_summary = issue['fields']['summary']
        issue_current_labels = issue['fields']['labels'] or []

        for shortcut, label_name in self.LABELS:
            if shortcut in issue_summary and label_name not in issue_current_labels:
                issue_key = issue['key']
                fields = {"labels": [{"add": label_name}]}
                try:
                    jira_obj.edit_issue(issue_key, fields, notify_users=False)
                    logging.info(f"Issue {issue_key}: {issue_summary} - added label: {label_name}")
                except Exception as exc:
                    logging.error(f"Error while updating issue {issue_key}: {exc}")