from director import Director
from repositories.company_repository import CompanyRepository
from config.database import Session
import multiprocessing
from enums.source import Source as SourceEnum

session = Session()

company_repository = CompanyRepository(session)
companies = [
    # Workable
    company_repository.get_random_company_by_source(SourceEnum.WORKABLE),
    # Workday
    company_repository.get_random_company_by_source(SourceEnum.WORKDAY),
    # Phenom People
    company_repository.get_random_company_by_source(SourceEnum.PHENOM_PEOPLE),
]

def director_wrapper(company):
    director = Director(company, session)

    return director.run()

if __name__ == '__main__':
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(director_wrapper, companies)

session.close()
