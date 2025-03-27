from models.company import Company
from config.database import Session
from sqlalchemy import cast, Integer
from typing import Union

class CompanyMapper:
    def __init__(self):
        self.session = Session()

    def find(self, company_id: int) -> Union[Company, None]:
        try:
            company = self.session.query(Company).filter(cast(company_id, Integer) == Company.id).first()
            return company
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()