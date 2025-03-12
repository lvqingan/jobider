from errors.parser.key_not_found_exception import KeyNotFoundException
from crawler import Crawler
from saver import Saver
from enums.content_type import ContentType
import json

crawler = Crawler('https://jobs.workable.com/api/v1/companies/vRPpyitDngWFGJcorm5xDf')
saver = Saver(crawler.run(), ContentType.JSON)
file_path = saver.run()

with open(file_path, 'r') as file:
    json_data = json.load(file)

    if 'jobs' not in json_data:
        raise KeyNotFoundException(json_data, 'jobs')

    jobs_data: dict = json_data['jobs']
    job_urls = []

    for job_data in jobs_data:
        if 'url' not in job_data:
            raise KeyNotFoundException(job_data, 'url')
        job_urls.append(job_data['url'])

    print(job_urls)
