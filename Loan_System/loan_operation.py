from typing import Annotated
from fastapi import APIRouter,Depends
from Login.login import get_user_detail
from Login import *
from ORM_Models import *
from HTTP_Exception.exceptions import *

def get_session():
    with Session(engine) as session:
        yield session

loan_operation_router = APIRouter()

@loan_operation_router.post("/api/farmer/loan/create", response_model=LoanInfoExposeToFarmer)
def create_loan_request(token: Annotated[str,Depends(oauth2Scheme)], newLoanInfo: LoanInfoCreate, session: Session = Depends(get_session)):
    payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    validation_number = payload.get("vnum")
    user_type = "Farmer"
    user = get_user_detail(validation_number,user_type,session)
    if not user:
        raise user_not_found_exception
    new_loan = LoanInfoInDB(**newLoanInfo.model_dump(), timeline=[LoanTimeLineEvent.initial_submission()])
    session.add(new_loan)
    session.commit()
    session.refresh(new_loan)
    expose_data = new_loan.model_dump()
    lender_info = session.exec(select(LoanSharkInDB).where(LoanSharkInDB.aadharCard==new_loan.aadhaarId)).first()
    expose_data.update({"lenderName": f"{lender_info.name}", "lenderLogo": f"{lender_info.loansharkLogo}"})
    return LoanInfoExposeToFarmer(**expose_data)
    
@loan_operation_router.get("/api/farmer/loan/fetch/{farmerID}")
def fetch_farmer_loans(farmerID: str, token: Annotated[str,Depends(oauth2Scheme)], session: Session = Depends(get_session)):
    payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    validation_number = payload.get("vnum")
    user_type = "Farmer"
    user = get_user_detail(validation_number,user_type,session)
    if not user:
        raise user_not_found_exception

    statement = select(LoanInfoInDB).where(LoanInfoInDB.farmerId==validation_number)
    pre_processed_info = session.exec(statement).all()
    post_processed_info = []
    for info in pre_processed_info:
        expose_data = info.model_dump()
        lender_info = session.exec(select(LoanSharkInDB).where(LoanSharkInDB.aadharCard==info.aadhaarId)).first()
        expose_data.update({"lenderName": f"{lender_info.name}", "lenderLogo": f"{lender_info.loansharkLogo}"})
        post_processed_info.append(LoanInfoExposeToFarmer(**expose_data))
    return post_processed_info

