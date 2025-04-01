from abc import ABC, abstractmethod
from typing import Union


class CursorBasedPagination(ABC):
    @abstractmethod
    def get_cursor_parameter_name(self) -> str:
        """
        Get the parameter name used for cursor-based pagination
        :return: parameter name
        :rtype: str
        """
        pass

    @abstractmethod
    def get_cursor_parameter_value(self) -> Union[str, None]:
        """
        Get the parameter value used for cursor-based pagination
        :return: parameter value
        :rtype: Union[str, None]
        """
        pass
