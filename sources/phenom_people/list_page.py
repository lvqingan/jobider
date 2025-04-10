import math
import re
import json
from typing import Union, List
from bs4 import BeautifulSoup
from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.list_page.without_detail import WithoutDetail as WithoutDetailContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as LengthAwarePaginationContract
from enums.content_type import ContentType


class ListPage(
    ListPageContract,
    WithoutDetailContract,
    LengthAwarePaginationContract
):
    def get_unique_ids(self) -> List[str]:
        json_data = self.content

        jobs_data: list[dict] = json_data['data']['jobs']
        internal_ids = []

        for job_data in jobs_data:
            internal_ids.append(job_data['jobId'])

        return internal_ids

    def get_response_content_type(self) -> ContentType:
        return ContentType.HTML

    def _load_content(self, file_path: str):
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            script_tags = soup.find_all('script', type='text/javascript')
            for script in script_tags:
                script_text = script.get_text()
                match = re.search(r'phApp\.ddo\s*=\s*({.*?});', script_text, re.DOTALL)
                if match:
                    ddo_value = match.group(1)
                    try:
                        return json.loads(ddo_value)['eagerLoadRefineSearch']
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error: {e}")

    def get_links_of_detail_pages(self, filtered_unique_ids: List[str]) -> List[str]:
        json_data = self.content

        jobs_data: list[dict] = json_data['data']['jobs']
        job_urls = []
        base_url = self.link_address.rsplit('/', 1)[0]

        for job_data in jobs_data:
            if job_data['jobId'] in filtered_unique_ids:
                job_urls.append(
                    '/'.join([base_url, 'job', job_data['jobId'], self.get_formatted_title(job_data['title'])]))

        return job_urls

    def get_remain_length_aware_parameters(self) -> Union[list, None]:
        json_data = self.content

        pages = math.ceil(json_data['totalHits'] / json_data['hits'])

        if pages > 1:
            params = []
            for i in range(1, pages):
                params.append({
                    'from': i * json_data['hits'],
                    's': 1
                })
            return params
        else:
            return None

    @staticmethod
    def get_formatted_title(title: str):
        formatted_title = title.lower()
        formatted_title = re.sub(r'[$_|`$-+:,/#&\[\]@{}*%.()?–\']', '-', formatted_title)
        formatted_title = re.sub(r' ', '-', formatted_title)
        formatted_title = re.sub(r'-+', '-', formatted_title)
        if formatted_title.endswith('-'):
            formatted_title = formatted_title[: -1]

        return formatted_title

    def use_external_id_as_unique_id(self) -> bool:
        return True
