from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, issue: dict, jira_obj):
        pass
