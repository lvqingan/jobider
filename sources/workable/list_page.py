import json
import re
from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.list_page.without_detail import WithoutDetail as WithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from contracts.list_page.cursor_based_pagination import CursorBasedPagination as CursorBasedPaginationContract
from typing import List, Union
from enums.content_type import ContentType
from errors.parser.key_not_found_exception import KeyNotFoundException


class ListPage(
    ListPageContract,
    WithoutDetailContract,
    PostRequestContract,
    CursorBasedPaginationContract
):
    def load_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {file_path}: {e}")

    def get_links_of_detail_pages(self, filtered_unique_ids: List[str]) -> List[str]:
        match = re.search(r'/accounts/([^/]+)/jobs', self.link_address)
        company_name_part = match.group(1)

        json_data = self.content

        if 'results' not in json_data:
            raise KeyNotFoundException(json_data, 'results')

        jobs_data: list[dict] = json_data['results']
        job_urls = []

        for job_data in jobs_data:
            if 'shortcode' not in job_data:
                raise KeyNotFoundException(job_data, 'shortcode')

            if str(job_data['id']) in filtered_unique_ids:
                job_urls.append(
                    f'https://apply.workable.com/api/v2/accounts/{company_name_part}/jobs/{job_data['shortcode']}')

        return job_urls

    def get_unique_ids(self) -> List[str]:
        json_data = self.content

        if 'results' not in json_data:
            raise KeyNotFoundException(json_data, 'results')

        jobs_data: list[dict] = json_data['results']
        internal_ids = []

        for job_data in jobs_data:
            if 'id' not in job_data:
                raise KeyNotFoundException(job_data, 'id')
            internal_ids.append(str(job_data['id']))

        return internal_ids

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
        json_data = self.content

        return json_data['nextPage'] if 'nextPage' in json_data else None
