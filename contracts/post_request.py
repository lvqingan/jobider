from abc import ABC, abstractmethod
from typing import Union


class PostRequest(ABC):
    @abstractmethod
    def get_request_payload(self) -> Union[dict, None]:
        """
        Get the request payload data that needs to be submitted when making a POST request
        :return: All payload data
        :rtype: Union[dict, None]
        """
        pass
