from abc import ABC, abstractmethod
from typing import List


class WithoutDetail(ABC):
    @abstractmethod
    def get_links_of_detail_pages(self, filtered_unique_ids: List[str]) -> List[str]:
        pass
