from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base


class CompanyDetail(Base):
    __tablename__ = 'company_details'
    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    logo = Column(String)
    about = Column(String)
    website = Column(String)
    industry = Column(String)
    company_size = Column(String)
    country = Column(String)
    city = Column(String)
    founded = Column(String)
    linkedin = Column(String)
    facebook = Column(String)
    youtube = Column(String)
    instagram = Column(String)
    twitter = Column(String)