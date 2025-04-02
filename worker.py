import random
from time import sleep
from typing import Union
from models.company import Company
from contracts.list_page.without_detail import WithoutDetail as ListPageWithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from contracts.source import Source as SourceContract
from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.detail_page import DetailPage as DetailPageContract
from contracts.list_page.cursor_based_pagination import CursorBasedPagination as ListPageCursorBasedPaginationContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as ListPageLengthAwarePaginationContract
from crawler import Crawler
from enums.request_method import RequestMethod
from repositories.job_repository import JobRepository
from saver import Saver
from urllib.parse import urlencode
import concurrent.futures


class Worker:
    def __init__(self, company: Company, source: SourceContract, session, next_page_parameters: dict = None):
        self.company = company
        self.session = session
        self.source = source
        self.next_page_parameters = next_page_parameters

    def run(self) -> Union[
        ListPageContract, ListPageCursorBasedPaginationContract, ListPageLengthAwarePaginationContract]:
        print(f'List Page Link: {self.company.index_url}')
        print(f'Next Page: {self.next_page_parameters if self.next_page_parameters is not None else 'None'}')
        list_page = self.source.get_list_page()

        if isinstance(list_page, PostRequestContract):
            request_payload = list_page.get_request_payload()
            if request_payload is None:
                request_payload = {}

            if self.next_page_parameters is not None:
                request_payload.update(self.next_page_parameters)
            list_crawler = Crawler(self.company.index_url, RequestMethod.POST, request_payload)
        else:
            if self.next_page_parameters is not None:
                list_crawler = Crawler(self.company.index_url + '?' + urlencode(self.next_page_parameters),
                                       RequestMethod.GET)
            else:
                list_crawler = Crawler(self.company.index_url, RequestMethod.GET)
        list_saver = Saver(list_crawler.run(), list_page.get_response_content_type())
        list_page.load(list_saver.run(), self.company.index_url)

        detail_page_links = []

        if isinstance(list_page, ListPageWithoutDetailContract):
            detail_page_links = list_page.get_links_of_detail_pages()

        if len(detail_page_links) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                detail_pages = list(executor.map(self._scrape_detail_pages, detail_page_links))

            # session is not thread safe
            job_repository = JobRepository(self.session)
            for detail_page in detail_pages:
                job_repository.save_job(detail_page.to_job(self.company))

        return list_page

    def _scrape_detail_pages(self, detail_page_link) -> DetailPageContract:
        seconds = random.randint(4, 8)
        print(f'Detail Page Link: {detail_page_link}. Sleep {seconds} seconds')
        detail_page = self.source.get_detail_page()

        if isinstance(detail_page, PostRequestContract):
            detail_crawler = Crawler(detail_page_link, RequestMethod.POST)
        else:
            detail_crawler = Crawler(detail_page_link, RequestMethod.GET)
        detail_saver = Saver(detail_crawler.run(), detail_page.get_response_content_type())
        sleep(seconds)
        detail_page.load(detail_saver.run(), detail_page_link)

        return detail_page
