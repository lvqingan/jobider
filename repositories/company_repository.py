from typing import Union

from mappers.company_mapper import CompanyMapper
from models.company import Company
from contracts.source import Source as SourceContract
from enums.source import Source as SourceEnum
from models.company_detail import CompanyDetail
from project_path import ProjectRootSingleton
from utils import upper_to_snake
import importlib
import sys


class CompanyRepository:
    def __init__(self, session):
        self.mapper = CompanyMapper(session)

    def get_company_with_details(self, company_id: int) -> Union[Company, None]:
        return self.mapper.find(company_id)

    def get_random_company_by_source(self, source: SourceEnum) -> Company:
        return self.mapper.random(source)

    @staticmethod
    def get_source(company: Company) -> SourceContract:
        source_enum = SourceEnum(company.source)

        sources_dir = ProjectRootSingleton().get_root_path() + '/sources/' + upper_to_snake(source_enum.name)
        sys.path.append(sources_dir)

        module = importlib.import_module('source')
        class_obj = getattr(module, 'Source')
        instance = class_obj()
        sys.path.remove(sources_dir)

        return instance

    def save(self, company: Company) -> Union[int, None]:
        return self.mapper.save(company)

    def save_detail(self, detail: CompanyDetail):
        self.mapper.save_detail(detail)