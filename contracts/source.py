from abc import ABC, abstractmethod
from contracts.list_page import ListPage as ListPageContract
from contracts.detail_page import DetailPage as DetailPageContract


class Source(ABC):
    @abstractmethod
    def get_list_page(self) -> ListPageContract:
        pass

    @abstractmethod
    def get_detail_page(self) -> DetailPageContract:
        pass

