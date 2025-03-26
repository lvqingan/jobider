from abc import ABC, abstractmethod
from contracts.list_page import ListPage as ListPageContract


class Source(ABC):
    @abstractmethod
    def get_list_page(self) -> ListPageContract:
        pass
