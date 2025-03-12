from enums.content_type import ContentType
import uuid


class Saver:
    def __init__(self, content: bytes, content_type: ContentType):
        """
        :param content: The content of the file that needs to be written
        :param content_type: The content type of the file to be written
        """
        self.content: bytes = content
        self.content_type: ContentType = content_type

    def run(self) -> str:
        """Execute the operation of writing to a temporary file
        :return: The save path of the temporary file
        :rtype: str
        """
        file_path = f'tmp/{str(uuid.uuid4())}.{'html' if self.content_type == ContentType.HTML else 'json'}'

        with open(file_path, 'wb') as file:
            file.write(self.content)

        return file_path
