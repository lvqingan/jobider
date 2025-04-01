import random
from time import sleep
from models.company import Company
from typing import Union
from contracts.list_page.without_detail import WithoutDetail as ListPageWithoutDetailContract
from contracts.post_request import PostRequest as PostRequestContract
from crawler import Crawler
from enums.request_method import RequestMethod
from repositories.job_repository import JobRepository
from saver import Saver
from urllib.parse import urlencode


class Worker:
    def __init__(self, company: Company, list_page, detail_page, session,
                 next_page_parameters: dict = None):
        self.company = company
        self.list_page = list_page
        self.detail_page = detail_page
        self.session = session
        self.next_page_parameters = next_page_parameters

    def run(self) -> Union[dict, list, None]:
        print(f'List Page Link: {self.company.index_url}')
        print(f'Next Page: {self.next_page_parameters if self.next_page_parameters is not None else 'None'}')

        if isinstance(self.list_page, PostRequestContract):
            request_payload = self.list_page.get_request_payload()
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
        list_saver = Saver(list_crawler.run(), self.list_page.get_response_content_type())
        self.list_page.load(list_saver.run(), self.company.index_url)

        detail_page_links = []

        if isinstance(self.list_page, ListPageWithoutDetailContract):
            detail_page_links = self.list_page.get_links_of_detail_pages()

        if len(detail_page_links) > 0:
            job_repository = JobRepository(self.session)

            for detail_page_link in detail_page_links:
                print(f'Detail Page Link: {detail_page_link}')

                if isinstance(self.detail_page, PostRequestContract):
                    detail_crawler = Crawler(detail_page_link, RequestMethod.POST)
                else:
                    detail_crawler = Crawler(detail_page_link, RequestMethod.GET)
                detail_saver = Saver(detail_crawler.run(), self.detail_page.get_response_content_type())
                seconds = random.randint(2, 7)
                print(f'Sleep {seconds} seconds')
                sleep(seconds)
                self.detail_page.load(detail_saver.run(), detail_page_link)

                job_repository.save_job(self.detail_page.to_job(self.company))
