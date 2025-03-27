from contracts.list_page_without_detail import ListPageWithoutDetail
from crawler import Crawler
from repositories.company_repository import CompanyRepository
from repositories.job_repository import JobRepository
from saver import Saver

company_repository = CompanyRepository()
company = company_repository.get_company_with_details(7)

if company:
    source = CompanyRepository.get_source(company)
    list_page = source.get_list_page()
    list_crawler = Crawler(company.index_url, list_page.get_request_method())
    list_saver = Saver(list_crawler.run(), list_page.get_content_type())
    list_page.file_path = list_saver.run()
    list_page.link_address = company.index_url

    detail_links = []

    if isinstance(list_page, ListPageWithoutDetail):
        detail_links = list_page.get_links_of_detail_pages()

    if len(detail_links) > 0:
        job_repository = JobRepository()

        for detail_link in detail_links:
            detail_page = source.get_detail_page()
            detail_crawler = Crawler(detail_link, detail_page.get_request_method())
            detail_saver = Saver(detail_crawler.run(), detail_page.get_content_type())
            detail_page.file_path = detail_saver.run()
            detail_page.link_address = detail_link

            job_repository.save_job(detail_page.to_job(company))