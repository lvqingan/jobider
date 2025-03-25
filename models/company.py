from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base
from models.company_detail import CompanyDetail


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer)
    source = Column(String)
    index_url = Column(String)
    request_method = Column(String)
    post_params = Column(String)

    details = relationship(CompanyDetail, backref='company', uselist=False)