from config.database import Session
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
