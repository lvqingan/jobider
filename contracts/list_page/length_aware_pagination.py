from abc import ABC, abstractmethod
from typing import Union


class LengthAwarePagination(ABC):
    @abstractmethod
    def get_remain_length_aware_parameters(self) -> Union[list, None]:
        """
        Get remain parameters used for length aware pagination
        :return: parameters
        :rtype: Union[list, None]
        """
        pass
