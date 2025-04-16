import json

from bs4 import BeautifulSoup
from contracts.detail_page import DetailPage as DetailPageContract
from enums.content_type import ContentType
from models.company import Company
from models.job import Job

from utils import convert_iso_to_mysql_datetime


class DetailPage(DetailPageContract):
    def _load_content(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def to_job(self, company: Company) -> Job:
        soup = BeautifulSoup(self.content, 'html.parser')
        json_data = json.loads(soup.find('script', type='application/ld+json').get_text())

        job = Job()
        job.company = company
        url = json_data['url']
        id_start = url.find('jobs/') + 5
        id_end = url.find('/', id_start)
        job.internal_id = url[id_start:id_end]
        job.title = json_data['title'].strip()

        if job.title == 'UNAVAILABLE' or job.title == '':
            job.title = soup.find('meta', property='og:title').get('content')

        job.description = json_data['description']
        job.employment_type = json_data['employmentType']
        job.url = url
        job.locations = []
        for job_location in json_data['jobLocation']:
            job.locations.append({
                'city': job_location['address']['addressLocality'],
                'region': job_location['address']['addressRegion'],
                'country': '',
                'country_code': job_location['address']['addressCountry'],
            })

        job.published_at = convert_iso_to_mysql_datetime(json_data['datePosted'])
        if 'jobLocationType' in json_data:
            job.workplace = json_data['jobLocationType']

        return job

    def get_response_content_type(self) -> ContentType:
        return ContentType.HTML
