from models.company import Company
from repositories.company_repository import CompanyRepository
from utils import log_exceptions
from worker import Worker
from config.database import Session
from contracts.list_page.cursor_based_pagination import CursorBasedPagination as ListPageCursorBasedPaginationContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as ListPageLengthAwarePaginationContract
import multiprocessing

session = Session()

company_repository = CompanyRepository(session)
companies = [
    company_repository.get_company_with_details(567),
    company_repository.get_company_with_details(25)
]

@log_exceptions
def crawl(company: Company):
    source = CompanyRepository.get_source(company)
    worker = Worker(company, source, session)
    list_page = worker.run()
    if isinstance(list_page, ListPageCursorBasedPaginationContract):
        cursor_parameter_value = list_page.get_cursor_parameter_value()

        while cursor_parameter_value is not None:
            next_page = Worker(company, source, session,
                               {list_page.get_cursor_parameter_name(): cursor_parameter_value}).run()

            cursor_parameter_value = next_page.get_cursor_parameter_value()
    elif isinstance(list_page, ListPageLengthAwarePaginationContract):
        remain_pages_parameters = list_page.get_remain_length_aware_parameters()

        if remain_pages_parameters is not None:
            for remain_pages_parameter in remain_pages_parameters:
                Worker(company, source, session, remain_pages_parameter).run()


if __name__ == '__main__':
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(crawl, companies)

session.close()
