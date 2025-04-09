import random
from typing import Union
from requests.adapters import HTTPAdapter
import requests
from urllib3 import Retry

from config.user_agents import USER_AGENTS
from enums.request_method import RequestMethod
from errors.crawler.request_timeout_exception import RequestTimeoutException
from errors.crawler.request_failed_exception import RequestFailedException


class Crawler:
    _timeout = 30

    def __init__(self, target_url: str, request_method: RequestMethod, request_payload: Union[dict, None] = None):
        """
        :param target_url: The target link address that needs to be crawled
        :param request_method: The request method of the target link
        :param request_payload: The POST request payload of the target link
        """
        self.target_url = target_url
        self.request_method = request_method
        self.request_payload = request_payload

    def run(self) -> bytes:
        """Execute network request tasks
        :return: The crawled web page content
        :rtype: bytes
        :exception RequestFailedException: The status code returned by the request is not 200
        :exception RequestTimeoutException: The request exceeds the set time limit
        """
        session = requests.Session()
        retry = Retry(connect=3, read=3, redirect=3, backoff_factor=0.3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }

        try:
            if self.request_method == RequestMethod.GET:
                response = session.get(self.target_url, headers=headers, timeout=self._timeout)
            else:
                if self.request_payload is None:
                    response = session.post(self.target_url, headers=headers, timeout=self._timeout)
                else:
                    response = session.post(self.target_url, headers=headers, timeout=self._timeout, json=self.request_payload)

            if response.status_code != requests.codes.ok:
                raise RequestFailedException(self.target_url, response.status_code)

            return response.content
        except requests.exceptions.Timeout as e:
            raise RequestTimeoutException(self.target_url, e.args)
