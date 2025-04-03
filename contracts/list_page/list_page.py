from abc import abstractmethod
from typing import List

from contracts.page import Page

class ListPage(Page):
    @abstractmethod
    def get_unique_ids(self) -> List[str]:
        pass

    def use_external_id_as_unique_id(self) -> bool:
        return False