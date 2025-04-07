from models.company import Company
from repositories.company_repository import CompanyRepository
from utils import log_exceptions
from worker import Worker
from contracts.list_page.cursor_based_pagination import CursorBasedPagination as ListPageCursorBasedPaginationContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as ListPageLengthAwarePaginationContract


class Director:
    def __init__(self, company: Company, session):
        self.company = company
        self.session = session

    @log_exceptions
    def run(self):
        source = CompanyRepository.get_source(self.company)
        worker = Worker(self.company, source, self.session)
        list_page = worker.run()
        if isinstance(list_page, ListPageCursorBasedPaginationContract):
            cursor_parameter_value = list_page.get_cursor_parameter_value()

            while cursor_parameter_value is not None:
                next_page = Worker(self.company, source, self.session,
                                   {list_page.get_cursor_parameter_name(): cursor_parameter_value}).run()

                cursor_parameter_value = next_page.get_cursor_parameter_value()
        elif isinstance(list_page, ListPageLengthAwarePaginationContract):
            remain_pages_parameters = list_page.get_remain_length_aware_parameters()

            if remain_pages_parameters is not None:
                for remain_pages_parameter in remain_pages_parameters:
                    Worker(self.company, source, self.session, remain_pages_parameter).run()