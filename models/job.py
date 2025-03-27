from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from models.company import Company


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    internal_id = Column(String(255), nullable=False)
    external_id = Column(String(255))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    employment_type = Column(String(50))
    benefits = Column(Text)
    requirements = Column(Text)
    url = Column(String(255), nullable=False)
    locations = Column(JSON)
    published_at = Column(DateTime)
    updated_at = Column(DateTime)
    workplace = Column(String(50))

    company = relationship(Company, backref='jobs')
