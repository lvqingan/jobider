from contracts.source import Source as SourceContract
from sources.workable.list_page import ListPage


class Source(SourceContract):
    def get_list_page(self) -> ListPage:
        return ListPage()