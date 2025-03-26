import importlib
from utils import upper_to_snake
from sqlalchemy.orm import Session
from contracts.source import Source as SourceContract
from enums.source import Source as SourceEnum
from models.company import Company
from project_path import ProjectRootSingleton
from repositories.company_repository import CompanyRepository
from config.database import Session
from sqlalchemy import cast, Integer
import sys


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

    def get_source(self, company:Company) -> SourceContract:
        source_enum = SourceEnum(company.source)

        sources_dir = ProjectRootSingleton().get_root_path() + '/sources/' + upper_to_snake(source_enum.name)
        sys.path.append(sources_dir)

        module = importlib.import_module('source')
        class_obj = getattr(module, 'Source')
        instance = class_obj()
        sys.path.remove(sources_dir)

        return instance