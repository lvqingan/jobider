from models.company import Company
from sqlalchemy import cast, Integer
from typing import Union
from enums.source import Source as SourceEnum
from sqlalchemy import func

class CompanyMapper:
    def __init__(self, session):
        self.session = session

    def find(self, company_id: int) -> Union[Company, None]:
        return self.session.query(Company).filter(cast(company_id, Integer) == Company.id).first()

    def random(self, source: SourceEnum) -> Company:
        return self.session.query(Company).filter(source.value == Company.source).order_by(func.rand()).first()