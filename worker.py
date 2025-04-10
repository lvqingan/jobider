import random
from time import sleep
from typing import Union

import html2text

from config.logging import worker_logger
from models.company import Company
from contracts.list_page.without_detail import WithoutDetail as ListPageWithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from contracts.source import Source as SourceContract
from contracts.list_page.list_page import ListPage as ListPageContract
from contracts.detail_page import DetailPage as DetailPageContract
from contracts.list_page.cursor_based_pagination import CursorBasedPagination as ListPageCursorBasedPaginationContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as ListPageLengthAwarePaginationContract
from contracts.modify_link import ModifyLink as ModifyLinkContract
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
        list_page = self.source.get_list_page()
        if isinstance(list_page, ModifyLinkContract):
            list_page.link_address = list_page.modify_link(self.company.index_url)
        else:
            list_page.link_address = self.company.index_url

        if self.next_page_parameters is not None:
            if isinstance(list_page, PostRequestContract):
                worker_logger.info(
                    f'Next Page Payload: {self.next_page_parameters if self.next_page_parameters is not None else 'None'}')
            else:
                if '?' in list_page.link_address:
                    list_page.link_address = list_page.link_address + '&' + urlencode(self.next_page_parameters)
                else:
                    list_page.link_address = list_page.link_address + '?' + urlencode(self.next_page_parameters)

        worker_logger.info(f'List Page Link: {list_page.link_address}')

        if isinstance(list_page, PostRequestContract):
            request_payload = list_page.get_request_payload()
            if request_payload is None:
                request_payload = {}

            if self.next_page_parameters is not None:
                request_payload.update(self.next_page_parameters)
            list_crawler = Crawler(list_page.link_address, RequestMethod.POST, request_payload)
        else:
            list_crawler = Crawler(list_page.link_address, RequestMethod.GET)
        list_saver = Saver(list_crawler.run(), list_page.get_response_content_type())
        list_page.load_content(list_saver.run())

        detail_page_links = []
        unique_ids = list_page.get_unique_ids()
        job_repository = JobRepository(self.session)
        if list_page.use_external_id_as_unique_id():
            filtered_unique_ids = job_repository.filter_out(self.company.id, external_ids=unique_ids)
        else:
            filtered_unique_ids = job_repository.filter_out(self.company.id, internal_ids=unique_ids)

        if isinstance(list_page, ListPageWithoutDetailContract):

            detail_page_links = list_page.get_links_of_detail_pages(filtered_unique_ids)

        if len(detail_page_links) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                detail_pages = list(executor.map(self._scrape_detail_pages, detail_page_links))

            # session is not thread safe
            for detail_page in detail_pages:
                job = detail_page.to_job(self.company)
                h = html2text.HTML2Text()
                job.description = h.handle(job.description)
                job_repository.save_job(job)

        return list_page

    def _scrape_detail_pages(self, detail_page_link) -> DetailPageContract:
        detail_page = self.source.get_detail_page()
        if isinstance(detail_page, ModifyLinkContract):
            detail_page.link_address = detail_page.modify_link(detail_page_link)
        else:
            detail_page.link_address = detail_page_link

        seconds = random.randint(4, 8)
        worker_logger.info(f'Detail Page Link: {detail_page.link_address}. Sleep {seconds} seconds')

        if isinstance(detail_page, PostRequestContract):
            detail_crawler = Crawler(detail_page.link_address, RequestMethod.POST)
        else:
            detail_crawler = Crawler(detail_page.link_address, RequestMethod.GET)
        detail_saver = Saver(detail_crawler.run(), detail_page.get_response_content_type())
        sleep(seconds)
        detail_page.load_content(detail_saver.run())

        return detail_page
