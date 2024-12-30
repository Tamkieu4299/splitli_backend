import csv

from constants.config import Settings
from models.geography import Geography
from sqlalchemy.ext.declarative import declarative_base

settings = Settings()


# Create an engine and a session
db = settings.psql_factory
smaker = db.create_sessionmaker()
session = smaker()

# Function to seed the database
def seed_geography_table(session, csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            geography = Geography(
                city=row['city'],
                city_ascii=row['city_ascii'],
                lat=float(row['lat']) if row['lat'] else None,
                lng=float(row['lng']) if row['lng'] else None,
                country=row['country'],
                iso2=row['iso2'],
                iso3=row['iso3'],
                admin_name=row['admin_name'],
                capital=row['capital'],
                population=int(float(row['population'])) if row['population'] else None
            )
            session.add(geography)
        session.commit()

# Seed the database
csv_file_path = './worldcities.csv'
seed_geography_table(session, csv_file_path)

# Close the session
session.close()
