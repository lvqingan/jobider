import math
import json
import time
from typing import Union, List
from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.list_page.without_detail import WithoutDetail as WithoutDetailContract
from contracts.modify_link import ModifyLink as ModifyLinkContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as LengthAwarePaginationContract
from enums.content_type import ContentType


class ListPage(
    ListPageContract,
    WithoutDetailContract,
    LengthAwarePaginationContract,
    ModifyLinkContract
):
    def get_unique_ids(self) -> List[str]:
        json_data = self.content

        jobs_data: list[dict] = json_data['jobRequisitions']
        internal_ids = []

        for job_data in jobs_data:
            internal_ids.append(job_data['itemID'])

        return internal_ids

    def get_response_content_type(self) -> ContentType:
        return ContentType.JSON

    def _load_content(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {file_path}: {e}")

    def get_links_of_detail_pages(self, filtered_unique_ids: List[str]) -> List[str]:
        json_data = self.content

        jobs_data: list[dict] = json_data['jobRequisitions']
        job_urls = []

        url = self.link_address.split('&timeStamp')[0]
        base_url = url.rsplit('?', 1)[0]
        cid = url.rsplit('?', 1)[1]

        for job_data in jobs_data:
            for string_field in job_data['customFieldGroup']['stringFields']:
                if string_field['nameCode']['codeValue'] == 'ExternalJobID':
                    external_id = string_field['stringValue']
                    if job_data['itemID'] in filtered_unique_ids:
                        job_urls.append(base_url + f"/{external_id}?" + cid)

        return job_urls

    def get_remain_length_aware_parameters(self) -> Union[list, None]:
        json_data = self.content

        if 'meta' in json_data:
            pages = math.ceil(json_data['meta']['totalNumber'] / 20)

            if pages > 1:
                params = []
                for i in range(1, pages):
                    params.append({
                        '$skip': i * 20 + 1,
                        'timeStamp': int(time.time() * 1000)
                    })
                return params

        return None

    def modify_link(self, link: str):
        return link + f'&timeStamp={int(time.time() * 1000)}&lang=en_US&locale=en_US&$top=20'
