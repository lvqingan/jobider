import json

from models.company import Company
from sqlalchemy import cast, Integer
from typing import Union
from enums.source import Source as SourceEnum
from sqlalchemy import func

from models.company_detail import CompanyDetail


class CompanyMapper:
    def __init__(self, session):
        self.session = session

    def find(self, company_id: int) -> Union[Company, None]:
        return self.session.query(Company).filter(cast(company_id, Integer) == Company.id).first()

    def random(self, source: SourceEnum) -> Company:
        return self.session.query(Company).filter(source.value == Company.source).order_by(func.rand()).first()

    def save(self, company: Company) -> Union[int, None]:
        try:
            company_model = Company(
                name=company.name,
                parent_id=company.parent_id,
                source=company.source,
                index_url=company.index_url,
                request_method=company.request_method,
                post_params=json.dumps(company.post_params) if company.post_params else None
            )
            self.session.add(company_model)
            self.session.commit()
            company.id = company_model.id
            return company.id
        except Exception as e:
            print(f"Error while inserting company: {e}")
            self.session.rollback()
            return None

    def save_detail(self, company_detail: CompanyDetail):
        try:
            company_detail_model = CompanyDetail(
                company_id=company_detail.company_id,
                logo=company_detail.logo,
                about=company_detail.about,
                website=company_detail.website,
                industry=company_detail.industry,
                company_size=company_detail.company_size,
                country=company_detail.country,
                city=company_detail.city,
                founded=company_detail.founded,
                linkedin=company_detail.linkedin,
                facebook=company_detail.facebook,
                youtube=company_detail.youtube,
                instagram=company_detail.instagram,
                twitter=company_detail.twitter
            )
            self.session.add(company_detail_model)
            self.session.commit()
        except Exception as e:
            print(f"Error while inserting company details: {e}")
            self.session.rollback()
