from abc import ABC, abstractmethod
from models.company import Company
from contracts.source import Source as SourceContract


class CompanyRepository(ABC):
    @abstractmethod
    def get_company_with_details(self, company_id):
        pass

    @abstractmethod
    def get_source(self, company:Company) -> SourceContract:
        pass