from contracts.source import Source as SourceContract
from sources.workforce_now.detail_page import DetailPage
from sources.workforce_now.list_page import ListPage


class Source(SourceContract):
    def get_list_page(self) -> ListPage:
        return ListPage()

    def get_detail_page(self) -> DetailPage:
        return DetailPage()