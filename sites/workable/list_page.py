from contracts.list_page import ListPage as ListPageContract
from errors.parser.key_not_found_exception import KeyNotFoundException
import json
from typing import List


class ListPage(ListPageContract):
    def get_links_of_detail_pages(self) -> List[str]:
        try:
            with open(self.file_path, 'r') as file:
                json_data = json.load(file)

                if 'jobs' not in json_data:
                    raise KeyNotFoundException(json_data, 'jobs')

                jobs_data: dict = json_data['jobs']
                job_urls = []

                for job_data in jobs_data:
                    if 'url' not in job_data:
                        raise KeyNotFoundException(job_data, 'url')
                    job_urls.append(job_data['url'])

                return job_urls
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {self.file_path}: {e}")