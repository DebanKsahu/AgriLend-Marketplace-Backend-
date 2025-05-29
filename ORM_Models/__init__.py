from ORM_Models.login_models import *
from ORM_Models.farmer_profile_models import *
from ORM_Models.loanshark_profile_models import *
from ORM_Models.farmer_production_models import *
from ORM_Models.loan_info_models import *
from sqlmodel import SQLModel,create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

MYSQL_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(url=MYSQL_URL,echo=True)