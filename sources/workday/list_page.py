import math

from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.list_page.without_detail import WithoutDetail as WithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as LengthAwarePaginationContract
from enums.content_type import ContentType
from errors.parser.key_not_found_exception import KeyNotFoundException
import json
from typing import List, Union


class ListPage(
    ListPageContract,
    WithoutDetailContract,
    PostRequestContract,
    LengthAwarePaginationContract
):
    _size = 20

    def _load_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {file_path}: {e}")

    def get_remain_length_aware_parameters(self) -> Union[list, None]:
        json_data = self.content
        pages = math.ceil(json_data['total'] / 20)

        if pages > 1:
            params = []
            for i in range(1, pages):
                params.append({
                    'offset': i * 20
                })

            return params
        else:
            return None

    def get_request_payload(self) -> dict:
        return {
            'appliedFacets': {},
            'limit': 20,
            'offset': 0,
            'searchText': ''
        }

    def get_response_content_type(self) -> ContentType:
        return ContentType.JSON

    def get_links_of_detail_pages(self, filtered_unique_ids: List[str]) -> List[str]:
        json_data = self.content

        if 'jobPostings' not in json_data:
            raise KeyNotFoundException(json_data, 'jobPostings')

        jobs_data: list[dict] = json_data['jobPostings']
        job_urls = []

        for job_data in jobs_data:
            if 'externalPath' not in job_data:
                raise KeyNotFoundException(job_data, 'externalPath')

            if 'bulletFields' not in job_data:
                raise KeyNotFoundException(job_data, 'bulletFields')

            if job_data['bulletFields'][0] in filtered_unique_ids:
                job_urls.append(self.link_address.rsplit('/', 1)[0] + job_data['externalPath'])

        return job_urls

    def get_unique_ids(self) -> List[str]:
        json_data = self.content

        if 'jobPostings' not in json_data:
            raise KeyNotFoundException(json_data, 'jobPostings')

        jobs_data: list[dict] = json_data['jobPostings']
        internal_ids = []

        for job_data in jobs_data:
            if 'bulletFields' not in job_data:
                raise KeyNotFoundException(job_data, 'bulletFields')
            internal_ids.append(str(job_data['bulletFields'][0]))

        return internal_ids

    def use_external_id_as_unique_id(self) -> bool:
        return True
