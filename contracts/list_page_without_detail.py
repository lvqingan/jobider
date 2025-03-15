from abc import ABC, abstractmethod
from typing import List


class ListPageWithoutDetail(ABC):
    @abstractmethod
    def get_links_of_detail_pages(self) -> List[str]:
        """
        Get all the links to the detail pages in the list page.
        The subsequent scripts will crawl the content of these links.
        :return: Links of all detail pages
        :rtype: List[str]
        """
        pass
