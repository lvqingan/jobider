from abc import ABC, abstractmethod
from typing import List


class WithDetail(ABC):
    @abstractmethod
    def get_details(self) -> List[dict]:
        """
        Parse and return all the detailed data from the data on the list page.
        :return: All detailed data
        :rtype: List[dict]
        """
        pass
