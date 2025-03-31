from models.company import Company
from sqlalchemy import cast, Integer
from typing import Union

class CompanyMapper:
    def __init__(self, session):
        self.session = session

    def find(self, company_id: int) -> Union[Company, None]:
        try:
            company = self.session.query(Company).filter(cast(company_id, Integer) == Company.id).first()
            return company
        except Exception as e:
            self.session.rollback()
            raise e