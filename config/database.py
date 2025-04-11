from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import get_config

config = get_config()
db_config = config['database']

engine = create_engine(
    f"mysql+pymysql://{db_config.get('user')}:{db_config.get('password')}@{db_config.get('host')}:{db_config.getint('port')}/{db_config.get('database')}")
Session = sessionmaker(bind=engine)

Base = declarative_base()
