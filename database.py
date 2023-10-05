import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, dotenv_values

db_config = dotenv_values(".env_shared")
db_config_pass = dotenv_values(".env_secret")

db_host = db_config['DB_HOST']
db_username = db_config['DB_USERNAME']
db_password = db_config_pass['DB_PASSWORD']
db_name = db_config['DB_NAME']

engine = create_engine(
    f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}",
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem",
        }
    }
)


def load_jobs():
    JOBS = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        for row in result.all():
            JOBS.append(row._asdict())
    return JOBS


def get_job(job_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :job_id"), {"job_id": job_id})
        for row in result.all():
            return row._asdict()
    return None


# noinspection PyArgumentList
def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url)"
            " VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

        conn.execute(query,
                     job_id=job_id,
                     full_name=data['full_name'],
                     email=data['email'],
                     linkedin_url=data['linkedin_url'],
                     education=data['education'],
                     work_experience=data['work_experience'],
                     resume_url=data['resume_url'])
