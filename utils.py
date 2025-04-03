import re
from datetime import datetime
import functools
from config.logging import worker_logger


def upper_to_snake(upper_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', upper_str)

    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_iso_to_mysql_datetime(s):
    dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def log_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            worker_logger.error(str(e))

    return wrapper