from bs4 import BeautifulSoup
from contracts.detail_page import DetailPage as DetailPageContract
from enums.content_type import ContentType
from models.company import Company
from models.job import Job
from rdflib import Graph
from rdflib.namespace import RDF, Namespace

from utils import convert_iso_to_mysql_datetime


class DetailPage(DetailPageContract):
    def _load_content(self, file_path):
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            return soup.find('script', type='application/ld+json').get_text()

    def to_job(self, company: Company) -> Job:
        json_data = self.content

        g = Graph()
        g.parse(data=json_data, format='json-ld')
        schema = Namespace('http://schema.org/')

        job = Job()
        job.company = company
        url = str(next((o for s, p, o in g.triples((None, schema.url, None))), None))
        id_start = url.find('jobs/') + 5
        id_end = url.find('/', id_start)
        job.internal_id = url[id_start:id_end]
        job.title = next((o for s, p, o in g.triples((None, schema.title, None))), None)
        job.description = next((o for s, p, o in g.triples((None, schema.description, None))), None)
        job.employment_type = next((o for s, p, o in g.triples((None, schema.employmentType, None))), None)
        job.url = url
        job.locations = []
        for s, p, o in g.triples((None, schema.jobLocation, None)):
            for sub_s, sub_p, sub_o in g.triples((o, schema.address, None)):
                job.locations.append({
                    'city': next((sub_sub_o for sub_sub_s, sub_sub_p, sub_sub_o in g.triples((sub_o, schema.addressLocality, None))), None),
                    'region': next((sub_sub_o for sub_sub_s, sub_sub_p, sub_sub_o in g.triples((sub_o, schema.addressRegion, None))), None),
                    'country': '',
                    'country_code': next((sub_sub_o for sub_sub_s, sub_sub_p, sub_sub_o in g.triples((sub_o, schema.addressCountry, None))), None),
                })
        job.published_at = convert_iso_to_mysql_datetime(next((o for s, p, o in g.triples((None, schema.datePosted, None))), None))
        job.workplace = next((o for s, p, o in g.triples((None, schema.jobLocationType, None))), None)

        return job

    def get_response_content_type(self) -> ContentType:
        return ContentType.HTML
