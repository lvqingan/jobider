import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from project_path import ProjectRootSingleton


def get_config():
    config = configparser.ConfigParser()
    config.read(ProjectRootSingleton().get_root_path() + '/config.ini')
    db_config = {
        'host': config.get('database', 'host'),
        'port': config.getint('database', 'port'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }
    return db_config


engine = create_engine(f"mysql+pymysql://{get_config()['user']}:{get_config()['password']}@{get_config()['host']}:{get_config()['port']}/{get_config()['database']}")
Session = sessionmaker(bind=engine)

Base = declarative_base()