import re
from bs4 import BeautifulSoup
from contracts.detail_page import DetailPage as DetailPageContract
from enums.content_type import ContentType
from models.company import Company
from models.job import Job
import json

from utils import convert_iso_to_mysql_datetime


class DetailPage(DetailPageContract):
    def load_content(self, file_path):
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            script_tags = soup.find_all('script', type='text/javascript')
            for script in script_tags:
                script_text = script.get_text()
                match = re.search(r'phApp\.ddo\s*=\s*({.*?});', script_text, re.DOTALL)
                if match:
                    ddo_value = match.group(1)
                    try:
                        return json.loads(ddo_value)['jobDetail']
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error: {e}")

    def to_job(self, company: Company) -> Job:
        json_data = self.content['data']['job']

        job = Job()
        job.company = company
        job.internal_id = json_data['jobSeqNo']
        job.external_id = json_data['jobId']
        job.title = json_data['title']
        job.description = json_data['description']
        job.employment_type = json_data['type']
        job.url = self.link_address
        job.locations = [{
            'city': json_data['city'],
            'region': json_data['state'],
            'country': json_data['country'],
            'country_code': '',
        }]
        job.published_at = convert_iso_to_mysql_datetime(json_data['postedDate'])
        job.updated_at = convert_iso_to_mysql_datetime(json_data['jobUpdatedDate'])
        if 'is_remote' in json_data:
            job.workplace = 'remote' if json_data['is_remote'] else 'on_site'

        return job

    def get_response_content_type(self) -> ContentType:
        return ContentType.HTML
