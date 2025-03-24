from config.database import Database as DatabaseConfig
import mysql.connector
from mysql.connector import Error as ConnectorError
import json
from models.company import Company
from models.company_detail import CompanyDetail


class CompanyMapper:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            db_config = DatabaseConfig.get_config()
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
        except ConnectorError as e:
            print(f"Error while connecting to database: {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def insert_company(self, company: Company):
        try:
            post_params_json = json.dumps(company.post_params) if company.post_params else None
            insert_query = "INSERT INTO companies (name, parent_id, source, index_url, request_method, post_params) " \
                           "VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_query, (company.name, company.parent_id, company.source, company.index_url,
                                               company.request_method, post_params_json))
            company.id = self.cursor.lastrowid
            self.connection.commit()
            return company.id
        except ConnectorError as e:
            print(f"Error while inserting company: {e}")
            self.connection.rollback()
            return None

    def insert_company_details(self, company_detail: CompanyDetail):
        try:
            insert_query = "INSERT INTO company_details (company_id, logo, about, website, industry, company_size, " \
                           "country, city, founded, linkedin, facebook, youtube, instagram, twitter) " \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_query, (company_detail.company_id, company_detail.logo, company_detail.about,
                                               company_detail.website, company_detail.industry,
                                               company_detail.company_size, company_detail.country,
                                               company_detail.city, company_detail.founded, company_detail.linkedin,
                                               company_detail.facebook, company_detail.youtube,
                                               company_detail.instagram,
                                               company_detail.twitter))
            self.connection.commit()
        except ConnectorError as e:
            print(f"Error while inserting company details: {e}")
            self.connection.rollback()
