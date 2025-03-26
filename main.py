from contracts.list_page_without_detail import ListPageWithoutDetail
from crawler import Crawler
from mappers.company_mapper import CompanyMapper
from saver import Saver

mapper = CompanyMapper()
company = mapper.get_company_with_details(7)

if company:
    source = mapper.get_source(company)
    list_page = source.get_list_page()

    crawler = Crawler(company.index_url, list_page.get_request_method())
    saver = Saver(crawler.run(), list_page.get_content_type())
    file_path = saver.run()

    list_page.file_path = file_path
    list_page.link_address = company.index_url

    detail_links = []

    if isinstance(list_page, ListPageWithoutDetail):
        detail_links = list_page.get_links_of_detail_pages()

    if len(detail_links) > 0:
        print(detail_links)