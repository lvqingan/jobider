from typing import List
from models.job import Job


class JobMapper:
    def __init__(self, session):
        self.session = session

    def save(self, job: Job):
        try:
            self.session.add(job)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def filter_out_by_internal_ids(self, company_id: int, internal_ids: List[str]) -> List[str]:
        existing_internal_ids = self.session.query(Job.internal_id).filter(
            Job.company_id == company_id,
            Job.internal_id.in_(internal_ids)
        ).all()
        existing_set = {id[0] for id in existing_internal_ids}

        return [id for id in internal_ids if id not in existing_set]

    def filter_out_by_external_ids(self, company_id: int, external_ids: List[str]) -> List[str]:
        existing_external_ids = self.session.query(Job.external_id).filter(
            Job.company_id == company_id,
            Job.external_id.in_(external_ids)
        ).all()
        existing_set = {id[0] for id in existing_external_ids}

        return [id for id in external_ids if id not in existing_set]
