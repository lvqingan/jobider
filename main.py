from repositories.company_repository import CompanyRepository
from worker import Worker
from config.database import Session

session = Session()

company_repository = CompanyRepository(session)
test_company = company_repository.get_company_with_details(567)

if test_company:
    next_page_parameter = Worker(test_company, session).run()

    while next_page_parameter is not None:
        next_page_parameter = Worker(test_company, session, next_page_parameter).run()

session.close()
