import random
from time import sleep
from models.company import Company
from typing import Union
from repositories.company_repository import CompanyRepository
from contracts.list_page_cursor_pagination import ListPageCursorPagination as ListPageCursorPaginationContract
from contracts.list_page_without_detail import ListPageWithoutDetail as ListPageWithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from crawler import Crawler
from enums.request_method import RequestMethod
from repositories.job_repository import JobRepository
from saver import Saver
from urllib.parse import urlencode


class Worker:
    def __init__(self, company: Company, session, next_page_parameter: dict = None):
        self.company = company
        self.session = session
        self.next_page_parameter = next_page_parameter

    def run(self) -> Union[dict, None]:
        print(f'List Page Link: {self.company.index_url}')
        print(f'Next Page: {self.next_page_parameter if self.next_page_parameter is not None else 'None'}')

        source = CompanyRepository.get_source(self.company)
        list_page = source.get_list_page()
        if isinstance(list_page, PostRequestContract):
            request_payload = list_page.get_request_payload()
            if request_payload is None:
                request_payload = {}

            if self.next_page_parameter is not None:
                request_payload.update(self.next_page_parameter)
            list_crawler = Crawler(self.company.index_url, RequestMethod.POST, request_payload)
        else:
            if self.next_page_parameter is not None:
                list_crawler = Crawler(self.company.index_url + '?' + urlencode(self.next_page_parameter),
                                       RequestMethod.GET)
            else:
                list_crawler = Crawler(self.company.index_url, RequestMethod.GET)
        list_saver = Saver(list_crawler.run(), list_page.get_response_content_type())
        list_page.file_path = list_saver.run()
        list_page.link_address = self.company.index_url

        detail_page_links = []

        if isinstance(list_page, ListPageWithoutDetailContract):
            detail_page_links = list_page.get_links_of_detail_pages()

        if len(detail_page_links) > 0:
            job_repository = JobRepository(self.session)

            for detail_page_link in detail_page_links:
                print(f'Detail Page Link: {detail_page_link}')

                detail_page = source.get_detail_page()
                if isinstance(detail_page, PostRequestContract):
                    detail_crawler = Crawler(detail_page_link, RequestMethod.POST)
                else:
                    detail_crawler = Crawler(detail_page_link, RequestMethod.GET)
                detail_saver = Saver(detail_crawler.run(), detail_page.get_response_content_type())
                seconds = random.randint(2, 7)
                print(f'Sleep {seconds} seconds')
                sleep(seconds)
                detail_page.file_path = detail_saver.run()
                detail_page.link_address = detail_page_link

                job_repository.save_job(detail_page.to_job(self.company))

        if isinstance(list_page, ListPageCursorPaginationContract):
            cursor_parameter_value = list_page.get_cursor_parameter_value()
            if cursor_parameter_value is not None:
                return {list_page.get_cursor_parameter_name(): cursor_parameter_value}
