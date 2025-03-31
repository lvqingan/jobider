import os
from abc import ABC, abstractmethod
from typing import Union
from enums.content_type import ContentType


class FilePath:
    """Descriptor class for managing file path.

    This class is used to control the setting and retrieval of the file path attribute.

    Attributes:
        value (Union[str, None]): The string storing the file path, initialized to None.
    """

    def __init__(self):
        self.value: Union[str, None] = None

    def __set__(self, instance, value):
        if not value:
            raise ValueError("file path cannot be empty.")
        if os.path.exists(value) and not os.path.isfile(value):
            raise ValueError("The provided path should be a file path.")
        self.value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.value is None:
            raise AttributeError("file path has not been set yet.")
        return self.value


class LinkAddress:
    def __init__(self):
        self.value: Union[str, None] = None

    def __set__(self, instance, value):
        if not value:
            raise ValueError("link address cannot be empty.")
        self.value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.value is None:
            raise AttributeError("link address has not been set yet.")
        return self.value


class Page(ABC):
    file_path: FilePath
    link_address: LinkAddress

    @abstractmethod
    def get_response_content_type(self) -> ContentType:
        """Get the content type of the list page for the current source
        :return: JSON or HTML
        :rtype: ContentType
        """
        pass
