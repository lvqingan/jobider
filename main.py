import random
import requests
from errors.crawler.request_failed_exception import RequestFailedException
from errors.crawler.request_timeout_exception import RequestTimeoutException
from errors.parser.key_not_found_exception import KeyNotFoundException

from config.user_agents import USER_AGENTS

headers = {
    "User-Agent": random.choice(USER_AGENTS)
}
target_url = 'https://jobs.workable.com/api/v1/companies/vRPpyitDngWFGJcorm5xDf'

try:
    response = requests.get(target_url, headers=headers, timeout=5)

    if response.status_code != requests.codes.ok:
        raise RequestFailedException(target_url, response.status_code)

    json_data = response.json()
    if 'jobs' not in json_data:
        raise KeyNotFoundException(json_data, 'jobs')

    jobs_data = json_data['jobs']
    job_urls = []

    for job_data in jobs_data:
        if 'url' not in job_data:
            raise KeyNotFoundException(job_data, 'url')
        job_urls.append(job_data['url'])

    print(job_urls)
except requests.exceptions.Timeout as e:
    raise RequestTimeoutException(target_url, e.args)
