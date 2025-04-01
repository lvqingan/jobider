import os
from abc import ABC, abstractmethod
from typing import Union
from enums.content_type import ContentType


class Content:
    def __init__(self):
        self.value: Union[str, None] = None

    def __set__(self, instance, value):
        if not value:
            raise ValueError("content cannot be empty.")
        self.value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.value is None:
            raise AttributeError("content has not been set yet.")
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
    link_address: LinkAddress
    _content: Content

    @abstractmethod
    def get_response_content_type(self) -> ContentType:
        """Get the content type of the list page for the current source
        :return: JSON or HTML
        :rtype: ContentType
        """
        pass

    @abstractmethod
    def load_content(self, file_path: str):
        pass

    def load(self, file_path: str, link_address: str):
        if os.path.exists(file_path) and not os.path.isfile(file_path):
            raise ValueError("The provided path should be a file path.")

        self._content = self.load_content(file_path)
        self.link_address = link_address

    def get_content(self):
        return self._content
