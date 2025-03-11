from errors.error_codes import CrawlerErrorCodes

class RequestTimeoutException(Exception):
    def __init__(self, target_url, time_used, message = None):
        self.target_url = target_url
        self.time_used = time_used
        self.error_code = CrawlerErrorCodes.REQUEST_TIMEOUT
        if message is None:
            self.message = f'[{time_used}s] {target_url}'
        else:
            self.message = message
        super().__init__(self.message)