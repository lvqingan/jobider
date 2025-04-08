from contracts.source import Source as SourceContract
from sources.phenom_people.detail_page import DetailPage
from sources.phenom_people.list_page import ListPage


class Source(SourceContract):
    def get_list_page(self) -> ListPage:
        return ListPage()

    def get_detail_page(self) -> DetailPage:
        return DetailPage()