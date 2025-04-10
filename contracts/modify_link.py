from abc import ABC, abstractmethod


class ModifyLink(ABC):
    @abstractmethod
    def modify_link(self, link: str) -> str:
        pass
