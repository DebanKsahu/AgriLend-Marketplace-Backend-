from typing import Annotated
from fastapi import APIRouter, Depends
from Login import *
from Login.login import get_user_detail
from ORM_Models import *