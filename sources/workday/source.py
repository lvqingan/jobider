from contracts.source import Source as SourceContract
from sources.workday.detail_page import DetailPage
from sources.workday.list_page import ListPage


class Source(SourceContract):
    def get_list_page(self) -> ListPage:
        return ListPage()

    def get_detail_page(self) -> DetailPage:
        return DetailPage()