from typing import Union, List
from urllib.parse import urlparse, parse_qs, unquote

from bs4 import BeautifulSoup
from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.list_page.without_detail import WithoutDetail as WithoutDetailContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as LengthAwarePaginationContract
from contracts.modify_link import ModifyLink as ModifyLinkContract
from enums.content_type import ContentType


class ListPage(
    ListPageContract,
    WithoutDetailContract,
    LengthAwarePaginationContract,
    ModifyLinkContract
):
    def get_unique_ids(self) -> List[str]:
        html_data = self.content

        soup = BeautifulSoup(html_data, 'html.parser')
        div_tag = soup.find('div', class_ = lambda x: x and 'iCIMS_JobsTable' in x)
        a_tags = div_tag.find_all('a', class_='iCIMS_Anchor')
        internal_ids = []
        for a_tag in a_tags:
            link = a_tag['href']
            id_start = link.find('jobs/') + 5
            id_end = link.find('/', id_start)
            internal_ids.append(link[id_start:id_end])

        return internal_ids

    def get_response_content_type(self) -> ContentType:
        return ContentType.HTML

    def _load_content(self, file_path: str):
        with open(file_path, 'r') as file:
            return file.read()

    def get_links_of_detail_pages(self, filtered_unique_ids: List[str]) -> List[str]:
        html_data = self.content

        soup = BeautifulSoup(html_data, 'html.parser')
        div_tag = soup.find('div', class_ = lambda x: x and 'iCIMS_JobsTable' in x)
        a_tags = div_tag.find_all('a', class_='iCIMS_Anchor')
        job_urls = []
        for a_tag in a_tags:
            link = a_tag['href']
            id_start = link.find('jobs/') + 5
            id_end = link.find('/', id_start)
            if link[id_start:id_end] in filtered_unique_ids:
                job_urls.append(a_tag['href'])

        return job_urls

    def get_remain_length_aware_parameters(self) -> Union[list, None]:
        html_data = self.content

        soup = BeautifulSoup(html_data, 'html.parser')
        div_tag = soup.find('div', class_=lambda x: x and 'iCIMS_PagingBatch' in x)

        if div_tag is not None:
            a_tags = div_tag.find_all('a')

            if len(a_tags) > 1:
                params = []
                for a_tag in a_tags:
                    parsed_url = urlparse(unquote(a_tag['href']))
                    raw_param = parse_qs(parsed_url.query)
                    param = {key: value[0] if value else None for key, value in raw_param.items()}
                    params.append(param)

                # The pagination of iCIMS by default includes the link to the first page.
                params.pop(0)

                return params

        return None

    def modify_link(self, link: str):
        return link + '?mobile=false&width=1290&height=500&bga=true&needsRedirect=false&jan1offset=480&jun1offset=480&in_iframe=1'
