from .strategy_interface import Strategy
import logging

class AddComponentsStrategy(Strategy):
    COMPONENTS = [
        ("[B]", "Backend"),
        ("[F]", "Frontend"),
    ]

    def execute(self, issue: dict, jira_obj):
        issue_summary = issue['fields']['summary']
        issue_current_components = issue['fields']['components'] or []
        current_component_names = [comp['name'] for comp in issue_current_components]

        for shortcut, component_name in self.COMPONENTS:
            if shortcut in issue_summary and component_name not in current_component_names:
                issue_key = issue['key']
                fields = {"components": [{"add": {"name": component_name}}]}
                try:
                    jira_obj.edit_issue(issue_key, fields, notify_users=False)
                    logging.info(f"Issue {issue_key}: {issue_summary} - added component: {component_name}")
                except Exception as exc:
                    logging.error(f"Error while updating issue {issue_key}: {exc}")
