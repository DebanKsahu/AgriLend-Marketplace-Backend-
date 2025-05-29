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

@loan_operation_router.post("/api/loan/create", response_model=LoanInfoExposeToFarmer)
def create_loan_request(token: Annotated[str,Depends(oauth2Scheme)], newLoanInfo: LoanInfoCreate, session: Session = Depends(get_session)):
    payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    validation_number = payload.get("vnum")
    user_type = "Farmer"
    user = get_user_detail(validation_number,user_type,session)
    if not user:
        raise user_not_found_exception
    
    new_loan = LoanInfoInDB(**newLoanInfo.model_dump())
    session.add(new_loan)
    session.commit()
    session.refresh(new_loan)

    new_timeline_entry = LoanTimeLineEventsInDB(
        loanInfoId=new_loan.id,
        date = date.today(),
        event= Event.APPLICATION_SUBMITTED,
        status= Status.PENDING
    )
    session.add(new_timeline_entry)
    session.commit()
    session.refresh(new_timeline_entry)
    return new_loan
    
@loan_operation_router.get("/api/farmer/loan/fetch/{farmerID}")
def fetch_farmer_loans(farmerID: str, token: Annotated[str,Depends(oauth2Scheme)], session: Session = Depends(get_session)) -> List[LoanInfoExposeToFarmer]:
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
        timeline_statement = select(LoanTimeLineEventsInDB).where(LoanTimeLineEventsInDB.loanInfoId==info.id)
        timeline_infos = session.exec(timeline_statement).all()
        lender_info = session.exec(select(LoanSharkInDB).where(LoanSharkInDB.aadharCard==info.aadhaarId)).first()
        expose_data = info.model_dump() 
        expose_data.update({"lenderName": f"{lender_info.name}", "lenderLogo": f"{lender_info.loansharkLogo}"})
        temp = []
        for timeline in timeline_infos:
            temp.append(LoanTimeLineEvent(**timeline.model_dump()))
        expose_data.update({"timeline": temp})
        post_processed_info.append(LoanInfoExposeToFarmer(**expose_data))
    return post_processed_info

@loan_operation_router.get("/api/loanshark/loan/fetch/{aadhaarCard}")
def fetch_lender_loan(aadhaarCard: str, token: Annotated[str,Depends(oauth2Scheme)], session: Session = Depends(get_session)) -> List[LoanInfoExposeToLender]:
    payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    validation_number = payload.get("vnum")
    user_type = "Farmer"
    user = get_user_detail(validation_number,user_type,session)
    if not user:
        raise user_not_found_exception 
    statement = select(LoanInfoInDB).where(LoanInfoInDB.aadhaarId==validation_number)
    pre_processed_info = session.exec(statement).all()
    post_processed_info = []
    for info in pre_processed_info:
        expose_data = info.model_dump()
        farmer_name = session.exec(select(FarmerInDB).where(FarmerInDB.digitalId==info.farmerId)).first()
        expose_data.update({"farmerName": f"{farmer_name.name}"})
        post_processed_info.append(LoanInfoExposeToLender(**expose_data))
    return post_processed_info

@loan_operation_router.patch("/api/loanshark/loans/approve/${id}")
def approve_loan(id: str, session: Session = Depends(get_session)):
    statement = select(LoanInfoInDB).where(LoanInfoInDB.id==id)
    result = session.exec(statement).one()
    result.status = Status.APPROVED
    session.add(result)
    session.commit()
    session.refresh(result)
    return {"message": "Application Approved", "success": True}

@loan_operation_router.patch("/api/loanshark/loans/reject/${id}")
def reject_loan(id: str, session: Session = Depends(get_session)):
    statement = select(LoanInfoInDB).where(LoanInfoInDB.id==id)
    result = session.exec(statement).one()
    result.status = Status.REJECTED
    session.add(result)
    session.commit()
    session.refresh(result)
    return {"message": "Application Rejected", "success": True}    