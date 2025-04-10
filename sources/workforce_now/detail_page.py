import time
from urllib.parse import urlparse, parse_qs, urlunparse
from contracts.detail_page import DetailPage as DetailPageContract
from enums.content_type import ContentType
from models.company import Company
from models.job import Job
import json
from utils import convert_iso_to_mysql_datetime
from contracts.modify_link import ModifyLink as ModifyLinkContract

class DetailPage(DetailPageContract, ModifyLinkContract):
    def _load_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {file_path}: {e}")

    def to_job(self, company: Company) -> Job:
        json_data = self.content

        job = Job()
        job.company = company
        job.internal_id = json_data['itemID']

        for string_field in json_data['customFieldGroup']['stringFields']:
            if string_field['nameCode']['codeValue'] == 'ExternalJobID':
                job.external_id = string_field['stringValue']

        job.title = json_data['requisitionTitle']
        job.description = json_data['requisitionDescription'].encode('utf-8').decode('unicode_escape')
        if 'workLevelCode' in json_data:
            job.employment_type = json_data['workLevelCode']['shortName']
        job.url = self.transform_url()
        if 'requisitionLocations' in json_data:
            job.locations = []
            for requisitionLocation in json_data['requisitionLocations']:
                job.locations.append({
                    'city': requisitionLocation['address']['cityName'],
                    'region': requisitionLocation['address']['countrySubdivisionLevel1']['codeValue'],
                    'country': '',
                    'country_code': '',
                })
        if 'postDate' in json_data:
            job.published_at = convert_iso_to_mysql_datetime(json_data['postDate'])

        return job

    def get_response_content_type(self) -> ContentType:
        return ContentType.JSON

    def modify_link(self, link: str):
        return link + f'&timeStamp={int(time.time() * 1000)}&lang=en_US&locale=en_US'

    def transform_url(self):
        parsed = urlparse(self.link_address)
        query_params = parse_qs(parsed.query)
        cid = query_params.get('cid', [''])[0]
        lang = query_params.get('lang', [''])[0]
        job_id = parsed.path.split('/')[-1]
        new_path = '/mascsr/default/mdf/recruitment/recruitment.html'
        new_query = f'cid={cid}&lang={lang}&selectedMenuKey=CurrentOpenings&jobId={job_id}'
        new_parsed = parsed._replace(path=new_path, query=new_query)

        return urlunparse(new_parsed)
