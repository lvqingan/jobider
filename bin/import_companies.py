import configparser
import mysql.connector
from mysql.connector import Error
import json


def read_db_config():
    config = configparser.ConfigParser()
    config.read('../config.ini')

    db_config = {
        'host': config.get('database', 'host'),
        'port': config.getint('database', 'port'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }
    return db_config


def insert_companies_and_details(company_name, logo_path, about, website, industry, company_size, country, city,
                                 founded,
                                 linkedin, facebook, youtube, instagram, twitter, source, index_url,
                                 request_method, post_params=None):
    db_config = read_db_config()
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            with open(logo_path, 'rb') as f:
                logo_data = f.read()

            if post_params is None:
                post_params = None
            else:
                post_params = json.dumps(post_params)
            insert_company_query = "INSERT INTO companies (name, source, index_url, request_method, post_params) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_company_query, (company_name, source, index_url, request_method, post_params))
            company_id = cursor.lastrowid

            insert_detail_query = "INSERT INTO company_details (company_id, logo, about, website, industry, company_size, " \
                                  "country, city, founded, linkedin, facebook, youtube, instagram, twitter) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_detail_query, (company_id, logo_data, about, website, industry, company_size,
                                                 country, city, founded, linkedin, facebook, youtube, instagram,
                                                 twitter))

            connection.commit()
            print("Data inserted successfully")

    except Error as e:
        print(f"Error while connecting to database or inserting data: {e}")
    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


# Example call
insert_companies_and_details('Sample Company Name', '../data/logos/1.jpeg', 'Description about the company',
                             'http://example.com', 'Industry', 'Company Size', 'Country', 'City',
                             2020, 'https://linkedin.com', 'https://facebook.com', 'https://youtube.com',
                             'https://instagram.com', 'https://twitter.com', 1, 'http://index.example.com', 'GET',
                             {'param1': 'value1'})
