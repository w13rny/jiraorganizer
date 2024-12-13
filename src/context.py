from strategies.strategy_interface import Strategy
from typing import Optional

class Context:
    def __init__(self, strategy: Optional[Strategy] = None):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def execute_strategy(self, issue: dict, jira_obj):
        if self._strategy is not None:
            self._strategy.execute(issue, jira_obj)
