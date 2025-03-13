"""
This module defines a set of classes for managing file paths and retrieving links from list pages.
The `FilePath` class is a descriptor for controlling file path attributes,
and the `ListPage` abstract class provides an interface for getting detail page links.
"""
from abc import ABC, abstractmethod
from typing import Union, List
import os


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


class ListPage(ABC):
    file_path: FilePath

    def set_file_path(self, file_path: str):
        """This method must be called to set the file path after instantiation.
        :param file_path: The file path used to parse the links
        """
        self.file_path = file_path

    @abstractmethod
    def get_links_of_detail_pages(self) -> List[str]:
        """
        Get all the links to the detail pages in the list page.
        The subsequent scripts will crawl the content of these links.
        :return: Links of all detail pages
        :rtype: List[str]
        """
        pass
