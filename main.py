from director import Director
from repositories.company_repository import CompanyRepository
from config.database import Session
import multiprocessing

session = Session()

company_repository = CompanyRepository(session)
companies = [
    company_repository.get_company_with_details(567),
    company_repository.get_company_with_details(25)
]

def director_wrapper(company):
    director = Director(company, session)

    return director.run()

if __name__ == '__main__':
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(director_wrapper, companies)

session.close()
