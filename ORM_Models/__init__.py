from ORM_Models.login_models import *
from ORM_Models.farmer_profile_models import *
from ORM_Models.loanshark_profile_models import *
from ORM_Models.farmer_production_models import *
from ORM_Models.loan_info_models import *
from sqlmodel import SQLModel,create_engine

MYSQL_URL = "mysql+mysqlconnector://deban:Horror@172.17.208.1:3306/servertesting"

engine = create_engine(url=MYSQL_URL,echo=True)