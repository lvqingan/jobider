from crawler import Crawler
from mappers.company_mapper import CompanyMapper
from enums.content_type import ContentType
from saver import Saver
from sources.workable.list_page import ListPage

mapper = CompanyMapper()
company = mapper.get_company_with_details(7)

if company:
    crawler = Crawler(company.index_url)
    saver = Saver(crawler.run(), ContentType.JSON)
    file_path = saver.run()

    list_page = ListPage()
    list_page.set_file_path(file_path)

    details = list_page.get_details()

    if len(details) > 0:
        print(details)