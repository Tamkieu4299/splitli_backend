from faker import Faker
from datetime import date
from models import Job, Vendor, User, BusinessCategory, Tags, JobTags, InternalUser, ApplicationStatus
from constants.config import Settings
import random

fake = Faker()
settings = Settings()

# Create an engine and a session
db = settings.psql_factory
smaker = db.create_sessionmaker()
session = smaker()

# Function to seed the vendors table with fake data
def seed_vendors_table(session, num_records=10):
    for _ in range(num_records):
        vendor = Vendor(
            name=fake.company(),
            phone=fake.phone_number(),
            email=fake.email(),
            password=fake.password(),
            city=fake.city(),
            country=fake.country(),
            address_1=fake.street_address(),
            address_2=fake.secondary_address(),
            avatar=fake.image_url(),
            background=fake.image_url(),
            general_info=fake.text(),
            industry=fake.word(),
            company_size=random.randint(1, 500),  # Random company size
            headquarter=fake.city(),
            business_type=fake.word(),
            business_license=fake.uuid4()  # Unique business license
        )
        session.add(vendor)
    session.commit()

# Function to seed the users table with fake data
def seed_users_table(session, num_records=10):
    for _ in range(num_records):
        user = User(
            user_name=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            phone=fake.phone_number(),
            gender=random.randint(0, 1),  # Assuming 0 or 1 for gender
            birthday=fake.date_of_birth(),
            email=fake.email(),
            city=fake.city(),
            country=fake.country(),
            address_1=fake.street_address(),
            address_2=fake.secondary_address(),
            avatar=fake.image_url()
        )
        session.add(user)
    session.commit()

# Function to seed the users table with fake data
def seed_internal_users_table(session, num_records=10):
    for _ in range(num_records):
        user = InternalUser(
            user_name=f"admin_{_}",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password="$2b$12$5RvW1YT7eFYmwX52Z5JYwOG9hzOGuza59lslnrHvUkrcJONZZciZq", #string
            phone=fake.phone_number(),
            email=f"admin{_}@gmail.com"
        )
        session.add(user)
    session.commit()

# Function to seed the jobs table with fake data
def seed_jobs_table(session, num_records=10, vendor_count=10, category_count=10):
    for _ in range(num_records):
        job = Job(
            title=fake.job(),
            description=fake.text(),
            requirements=fake.text(),
            benefits=fake.text(),
            salary_type=fake.word(ext_word_list=['fixed', 'negotiable']),
            level=fake.word(ext_word_list=['intern', 'fresher', 'no experience needed', 'junior', 'middle', 'senior']),
            payment_frequency=fake.word(ext_word_list=['hourly', 'daily', 'weekly', "monthly", "annually"]),
            min_salary=round(random.uniform(30000, 100000),2),  # Random salary range
            max_salary=round(random.uniform(100001, 200000), 2),
            picture=fake.image_url(),
            vendor_id=random.randint(1, vendor_count),  # Random vendor ID
            category_id=random.randint(1, category_count),  # Random category ID
            created_by=random.randint(1, 5),  # Assuming there are users already created
            positions_available=random.randint(1, 10),  # Random available positions
            address_1=fake.street_address(),
            address_2=fake.secondary_address(),
            country=fake.country(),
            city=fake.city(),
            created_at=fake.date_time_this_year(),
            start_date=fake.date_this_year(),
            end_date=fake.date_this_year(),
            currency=fake.currency_code(),  # Just a placeholder for currency
            is_deleted=False
        )
        session.add(job)
    session.commit()

# Function to seed the business categories table with fake data
def seed_business_categories_table(session, num_records=10, vendor_count=10):
    for _ in range(num_records):
        business_category = BusinessCategory(
            name=fake.word(ext_word_list=["Technology", "Property", "Healthcare", 
                                          "Finance", "Coffeeshop", "Business"]),
            vendor_id=random.randint(1, vendor_count)  # Random vendor ID
        )
        session.add(business_category)
    session.commit()

# Function to seed the tags table with fake data
def seed_tags_table(session, num_records=10):
    for _ in range(num_records):
        tag = Tags(
            key=fake.word(),
            label=fake.word(ext_word_list=['common', 'location']).capitalize(),
            description=fake.sentence(),
            value=fake.word()
        )
        session.add(tag)
    session.commit()

# Function to seed the job_tags table with fake data
def seed_job_tags_table(session, num_records=10, job_count=10, tag_count=10):
    for _ in range(num_records):
        job_tag = JobTags(
            job_id=random.randint(1, job_count),  # Random job ID
            tag_id=random.randint(1, tag_count)   # Random tag ID
        )
        session.add(job_tag)
    session.commit()

# Function to seed the status id table with fake data
def seed_status_table(session):
    name_list = ["pending", "viewed", "accepted", "denied"]

    for index, value in enumerate(name_list):
        application_status = ApplicationStatus(
            id = index,
            name = value
        )
        session.add(application_status)
    session.commit()

# Main function to call all seeding functions
def main_seeding(session):
    num_vendors = 10
    num_users = 10
    num_jobs = 50
    num_categories = 5
    num_tags = 10
    num_job_tags = 40
    num_internal_users = 5


    seed_vendors_table(session, num_vendors)
    seed_users_table(session, num_users)
    seed_business_categories_table(session, num_categories, num_vendors)
    seed_tags_table(session, num_tags)
    seed_jobs_table(session, num_jobs, num_vendors, num_categories)
    seed_job_tags_table(session, num_job_tags, num_jobs, num_tags)
    seed_internal_users_table(session, num_internal_users)
    seed_status_table(session)

# Execute the main seeding function
main_seeding(session)

# Close the session
session.close()
