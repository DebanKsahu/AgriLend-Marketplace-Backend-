import jwt
from fastapi import Depends, HTTPException, status, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session,select
from fastapi.security import OAuth2PasswordBearer

#----------GLOBAL VARIABLES/SETTINGS------------#
SECRET_KEY = "7165de02e0e87f1f89a7ab20598d39fc476383d23c529017fa55e107a7157480"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#--------------------------------------#
print("Login __INIT__ starting")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="api/farmer/login")