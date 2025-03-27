from mappers.job_mapper import JobMapper
from models.job import Job


class JobRepository:
    def __init__(self):
        self.mapper = JobMapper()

    def save_job(self, job: Job):
        self.mapper.save(job)