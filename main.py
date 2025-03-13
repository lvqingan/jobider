from crawler import Crawler
from saver import Saver
from enums.content_type import ContentType
from sites.workable.list_page import ListPage

crawler = Crawler('https://jobs.workable.com/api/v1/companies/vRPpyitDngWFGJcorm5xDf')
saver = Saver(crawler.run(), ContentType.JSON)
file_path = saver.run()

list_page = ListPage()
list_page.set_file_path(file_path)
print(list_page.get_links_of_detail_pages())
