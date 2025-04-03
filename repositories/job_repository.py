from typing import List

from mappers.job_mapper import JobMapper
from models.job import Job


class JobRepository:
    def __init__(self, session):
        self.mapper = JobMapper(session)

    def save_job(self, job: Job):
        self.mapper.save(job)

    def filter_out(self, company_id: int, internal_ids: List[str] = None, external_ids: List[str] = None) -> List[str]:
        if internal_ids is not None:
            return self.mapper.filter_out_by_internal_ids(company_id, internal_ids)
        elif external_ids is not None:
            return self.mapper.filter_out_by_external_ids(company_id, external_ids)
        else:
            raise TypeError("Only one of the two parameters, `internal_ids` or `external_ids`, must have a value.")