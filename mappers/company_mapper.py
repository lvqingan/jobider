from sqlalchemy.orm import Session
from models.company import Company
from repositories.company_repository import CompanyRepository
from config.database import Session
from sqlalchemy import cast, Integer


class CompanyMapper(CompanyRepository):
    def __init__(self):
        self.session = Session()

    def get_company_with_details(self, company_id):
        try:
            company = self.session.query(Company).filter(cast(company_id, Integer) == Company.id).first()
            return company
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()