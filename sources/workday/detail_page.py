from contracts.detail_page import DetailPage as DetailPageContract
from enums.content_type import ContentType
from models.company import Company
from models.job import Job
import json


class DetailPage(DetailPageContract):
    def load_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {file_path}: {e}")

    def to_job(self, company: Company) -> Job:
        json_data = self.get_content()['jobPostingInfo']

        job = Job()
        job.company = company
        job.internal_id = json_data['id']
        job.external_id = json_data['jobReqId']
        job.title = json_data['title']
        job.description = json_data['jobDescription']
        job.employment_type = json_data['timeType']
        job.url = json_data['externalUrl']
        if 'jobRequisitionLocation' in json_data:
            job.locations = [{
                'city': json_data['jobRequisitionLocation']['descriptor'],
                'region': '',
                'country': json_data['jobRequisitionLocation']['country']['descriptor'],
                'country_code': json_data['jobRequisitionLocation']['country']['alpha2Code'],
            }]
        job.published_at = json_data['startDate'] if 'startDate' in json_data else None
        job.expired_at = json_data['endDate'] if 'endDate' in json_data else None

        return job

    def get_response_content_type(self) -> ContentType:
        return ContentType.JSON
