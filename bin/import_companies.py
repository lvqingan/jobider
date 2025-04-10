import csv
import os
import json

from config.database import Session
from enums.source import Source
from models.company import Company
from models.company_detail import CompanyDetail
from tqdm import tqdm

from repositories.company_repository import CompanyRepository


def main():
    session = Session()
    company_repository = CompanyRepository(session)

    csv_file_path = '../data/companies.csv'
    logos_dir = '../data/logos'

    def csv_generator():
        with open(csv_file_path, 'r', encoding='utf8') as csv_generator_file:
            reader = csv.DictReader(csv_generator_file)
            for csv_row in reader:
                yield csv_row

    with open(csv_file_path, 'r', encoding='utf8') as csvfile:
        total_lines = sum(1 for _ in csv.reader(csvfile)) - 1

    for i, row in enumerate(tqdm(csv_generator(), total=total_lines)):
        source_str = row['Driver']

        try:
            source = Source(source_str)
        except ValueError:
            print(f"Invalid source value in CSV: {source_str}. Skipping this row.")
            continue

        index_url = row.get('ListUrl')

        if source == Source.WORKFORCE_NOW:
            note = json.loads(row.get('Note'))
            index_url = index_url + '?cid=' + note['identifier']

        company_data = {
            'name': row.get('Name'),
            'source': source.value,
            'index_url': index_url,
            'request_method': row.get('RequestType') if row.get('RequestType') else 'GET',
            'post_params': json.loads(row.get('Params') if row.get('Params') else '{}')
        }
        company = Company(**company_data)
        company_id = company_repository.insert(company)

        if company_id:
            logo_id = row.get('LogoID')
            logo_path = os.path.join(logos_dir, f'{logo_id}.jpeg')
            logo_data = None

            try:
                if os.path.exists(logo_path):
                    with open(logo_path, 'rb') as f:
                        logo_data = f.read()
            except (FileNotFoundError, PermissionError, OSError) as e:
                print(f"Error reading logo file {logo_path}: {e}. Using default logo data.")

            company_details_data = {
                'company_id': company_id,
                'logo': logo_data,
                'about': row.get('About'),
                'website': row.get('Website'),
                'industry': row.get('Industry'),
                'company_size': row.get('Size'),
                'country': 'USA',
                'city': row.get('City'),
                'founded': row.get('Founded'),
                'linkedin': row.get('LinkedIn'),
                'facebook': row.get('Facebook'),
                'youtube': row.get('Youtube'),
                'instagram': row.get('Instagram'),
                'twitter': row.get('Twitter')
            }
            company_details = CompanyDetail(**company_details_data)
            try:
                company_repository.insert_detail(company_details)
            except Exception as e:
                print(f"Error inserting company details: {e}. Skipping this company details.")

    session.close()


if __name__ == "__main__":
    main()
