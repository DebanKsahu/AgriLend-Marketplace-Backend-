from fastapi import FastAPI
from ORM_Models import SQLModel,engine
from contextlib import asynccontextmanager
from Login.login import login_router
from Profile.profile import profile_router
from Loan_System.loan_operation import loan_operation_router

print("Starting")
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(login_router, tags=["Login"])
app.include_router(profile_router,tags=["Profile"])
app.include_router(loan_operation_router,tags=["Loan Operations"])