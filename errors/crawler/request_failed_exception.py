from errors.error_codes import CrawlerErrorCodes

class RequestFailedException(Exception):
    def __init__(self, target_url, status_code, message = None):
        self.target_url = target_url
        self.status_code = status_code
        self.error_code = CrawlerErrorCodes.REQUEST_FAILED
        if message is None:
            self.message = f'[{status_code}] {target_url}'
        else:
            self.message = message
        super().__init__(self.message)