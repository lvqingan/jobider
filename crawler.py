import random
import requests
from config.user_agents import USER_AGENTS
from errors.crawler.request_timeout_exception import RequestTimeoutException
from errors.crawler.request_failed_exception import RequestFailedException


class Crawler:
    def __init__(self, target_url: str):
        """
        :param target_url: The target link address that needs to be crawled
        """
        self.target_url = target_url

    def run(self) -> bytes:
        """Execute network request tasks
        :return: The crawled web page content
        :rtype: bytes
        :exception RequestFailedException: The status code returned by the request is not 200
        :exception RequestTimeoutException: The request exceeds the set time limit
        """
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }

        try:
            response = requests.get(self.target_url, headers=headers, timeout=5)

            if response.status_code != requests.codes.ok:
                raise RequestFailedException(self.target_url, response.status_code)

            return response.content
        except requests.exceptions.Timeout as e:
            raise RequestTimeoutException(self.target_url, e.args)
