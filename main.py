from repositories.company_repository import CompanyRepository
from worker import Worker
from config.database import Session
from contracts.list_page.cursor_based_pagination import CursorBasedPagination as ListPageCursorBasedPaginationContract
from contracts.list_page.length_aware_pagination import LengthAwarePagination as ListPageLengthAwarePaginationContract

session = Session()

company_repository = CompanyRepository(session)
test_company = company_repository.get_company_with_details(567)
# test_company = company_repository.get_company_with_details(25)

if test_company:
    source = CompanyRepository.get_source(test_company)
    list_page = source.get_list_page()
    detail_page = source.get_detail_page()
    worker = Worker(test_company, list_page, detail_page, session)
    worker.run()

    if isinstance(list_page, ListPageCursorBasedPaginationContract):
        cursor_parameter_value = list_page.get_cursor_parameter_value()

        while cursor_parameter_value is not None:
            Worker(test_company, list_page, detail_page, session,
                   {list_page.get_cursor_parameter_name(): cursor_parameter_value}).run()

            cursor_parameter_value = list_page.get_cursor_parameter_value()
    elif isinstance(list_page, ListPageLengthAwarePaginationContract):
        remain_pages_parameters = list_page.get_remain_length_aware_parameters()

        if remain_pages_parameters is not None:
            for remain_pages_parameter in remain_pages_parameters:
                Worker(test_company, list_page, detail_page, session, remain_pages_parameter).run()

session.close()
