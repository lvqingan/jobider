import re
import traceback
from datetime import datetime
import functools
from config.logging import worker_logger
import configparser
from functools import lru_cache
from project_path import ProjectRootSingleton


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
        except Exception as _:
            worker_logger.error(traceback.format_exc())

    return wrapper

@lru_cache(maxsize = 1)
def get_config():
    config = configparser.ConfigParser()
    config.read(ProjectRootSingleton().get_root_path() + '/config.ini')

    return config