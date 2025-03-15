import json

import pytest
import requests
from unittest.mock import patch

from crawler import Crawler
from errors.crawler.request_failed_exception import RequestFailedException
from errors.crawler.request_timeout_exception import RequestTimeoutException
from errors.error_codes import CrawlerErrorCodes


class TestCrawler:
    def test_successful_requests_and_responses(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = requests.codes.ok
        data = {"key": "value"}
        mock_response.content = json.dumps(data).encode('utf8')

        with patch('crawler.requests.get', return_value=mock_response):
            crawler = Crawler("http://example.com")
            result = crawler.run()
            assert json.loads(result) == data

    def test_handle_request_timeouts(self):
        with patch('crawler.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout

            with pytest.raises(RequestTimeoutException) as e:
                crawler = Crawler("http://example.com")
                crawler.run()

            assert e.value.error_code == CrawlerErrorCodes.REQUEST_TIMEOUT
            assert e.value.target_url == "http://example.com"

    def test_handle_unsuccessful_requests(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = requests.codes.not_found

        with patch('crawler.requests.get', return_value=mock_response):
            with pytest.raises(RequestFailedException) as e:
                crawler = Crawler("http://example.com")
                crawler.run()

            assert e.value.error_code == CrawlerErrorCodes.REQUEST_FAILED
            assert e.value.status_code == requests.codes.not_found
