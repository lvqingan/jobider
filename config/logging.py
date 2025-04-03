from loguru import logger as base_logger
from project_path import ProjectRootSingleton


def create_custom_logger(sink):
    new_logger = base_logger.bind()
    new_logger.remove()
    new_logger.add(sink, format='{time} | {level} | {message}')

    return new_logger

worker_logger = create_custom_logger(ProjectRootSingleton().get_root_path() + '/logs/worker.log')