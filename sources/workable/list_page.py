import json
import re
from contracts.list_page import ListPage as ListPageContract
from contracts.list_page_without_detail import ListPageWithoutDetail as ListPageWithoutDetailContract
from typing import List

from enums.content_type import ContentType
from enums.request_method import RequestMethod
from errors.parser.key_not_found_exception import KeyNotFoundException


class ListPage(ListPageContract, ListPageWithoutDetailContract):
    def get_links_of_detail_pages(self) -> List[str]:
        match = re.search(r'/accounts/([^/]+)/jobs', self.link_address)
        company_name_part = match.group(1)

        try:
            with open(self.file_path, 'r') as file:
                json_data = json.load(file)

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
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {self.file_path}: {e}")

    def get_request_method(self) -> RequestMethod:
        return RequestMethod.POST

    def get_content_type(self) -> ContentType:
        return ContentType.JSON
