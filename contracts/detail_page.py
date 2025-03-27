from abc import abstractmethod
from contracts.page import Page
from models.company import Company
from models.job import Job


class DetailPage(Page):
    @abstractmethod
    def to_job(self, company: Company) -> Job:
        pass