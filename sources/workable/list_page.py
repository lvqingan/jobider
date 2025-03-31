import json
import re
from contracts.list_page import ListPage as ListPageContract
from contracts.list_page_without_detail import ListPageWithoutDetail as ListPageWithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from contracts.list_page_cursor_pagination import ListPageCursorPagination as ListPageCursorPaginationContract
from typing import List, Union
from enums.content_type import ContentType
from errors.parser.key_not_found_exception import KeyNotFoundException


class ListPage(
    ListPageContract,
    ListPageWithoutDetailContract,
    PostRequestContract,
    ListPageCursorPaginationContract
):
    _content = None

    def _get_content(self):
        if self._content is None:
            try:
                with open(self.file_path, 'r') as file:
                    self._content = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON in file {self.file_path}: {e}")
        return self._content

    def get_links_of_detail_pages(self) -> List[str]:
        match = re.search(r'/accounts/([^/]+)/jobs', self.link_address)
        company_name_part = match.group(1)

        json_data = self._get_content()

        if 'results' not in json_data:
            raise KeyNotFoundException(json_data, 'results')

        jobs_data: list[dict] = json_data['results']
        job_urls = []

        for job_data in jobs_data:
            if 'shortcode' not in job_data:
                raise KeyNotFoundException(job_data, 'shortcode')
            job_urls.append(
                f'https://apply.workable.com/api/v2/accounts/{company_name_part}/jobs/{job_data['shortcode']}')

        return job_urls

    def get_request_payload(self) -> dict:
        return {
            'query': '',
            'department': [],
            'location': [],
            'remote': [],
            'workplace': [],
            'worktype': []
        }

    def get_response_content_type(self) -> ContentType:
        return ContentType.JSON

    def get_cursor_parameter_name(self) -> str:
        return 'token'

    def get_cursor_parameter_value(self) -> Union[str, None]:
        json_data = self._get_content()

        return json_data['nextPage'] if 'nextPage' in json_data else None
