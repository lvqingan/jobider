import json

from contracts.list_page import ListPage as ListPageContract
from contracts.list_page_with_detail import ListPageWithDetail as ListPageWithDetailContract
from typing import List

from errors.parser.key_not_found_exception import KeyNotFoundException


class ListPage(ListPageContract, ListPageWithDetailContract):
    def get_details(self) -> List[dict]:
        try:
            with open(self.file_path, 'r') as file:
                json_data = json.load(file)

                if 'jobs' not in json_data:
                    raise KeyNotFoundException(json_data, 'jobs')

                job_details: list[dict] = json_data['jobs']

                return job_details
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {self.file_path}: {e}")