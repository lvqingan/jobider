from abc import ABC, abstractmethod
from models.company import Company


class CompanyRepository(ABC):
    @abstractmethod
    def get_company_with_details(self, company_id):
        pass