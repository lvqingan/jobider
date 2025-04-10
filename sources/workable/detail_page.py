from contracts.detail_page import DetailPage as DetailPageContract
from enums.content_type import ContentType
from models.company import Company
from models.job import Job
from utils import convert_iso_to_mysql_datetime
import json
import re


class DetailPage(DetailPageContract):
    def _load_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {file_path}: {e}")

    def to_job(self, company: Company) -> Job:
        match = re.search(r'/accounts/([^/]+)/jobs', self.link_address)
        company_name_part = match.group(1)

        json_data = self.content

        job = Job()
        job.company = company
        job.internal_id = json_data['id']
        job.external_id = json_data['code']
        job.title = json_data['title']
        job.description = json_data['description']
        job.employment_type = json_data['type'] if 'type' in json_data else None
        job.benefits = json_data['benefits']
        job.requirements = json_data['requirements']
        job.url = f'https://apply.workable.com/{company_name_part}/j/{json_data['shortcode']}/'
        job.locations = []

        if len(json_data['locations']) > 0:
            for location in json_data['locations']:
                job.locations.append({
                    'city': location['city'],
                    'region': location['region'],
                    'country': location['country'],
                    'country_code': location['countryCode'],
                })

        job.published_at = convert_iso_to_mysql_datetime(json_data['published'])
        job.workplace = json_data['workplace']

        return job

    def get_response_content_type(self) -> ContentType:
        return ContentType.JSON
