from Profile import *
from HTTP_Exception.exceptions import *

profile_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session

def retrive_profile_info(user_type: str, validation_number: str, session: Session):
    profile_detail = None
    if user_type=="Farmer":
        statement = select(FarmerInDB).where(FarmerInDB.digitalId==validation_number)
        profile_detail = session.exec(statement=statement).first()
        if profile_detail is not None:
            session.refresh(profile_detail)
            productivity_detail = retrive_farmer_productivity_record(validation_number,session)
            profile_data = profile_detail.model_dump(exclude={"hashed_password", "aadharCard", "dob", "bankAccount"})
            profile_data["productivityRecords"] = productivity_detail
            return FarmerProfile(**profile_data)
    elif user_type=="LoanShark":
        statement = select(LoanSharkProfile).where(LoanSharkProfile.aadharCard==validation_number)
        profile_detail = session.exec(statement=statement).first() 
        if profile_detail is not None:
            session.refresh(profile_detail)
            profile_data = profile_detail.model_dump(exclude={"hashed_password", "aadharCard", "dob", "bankAccount"})
            return LoanSharkProfile(**profile_data) 
    if profile_detail is None:
        raise user_profile_not_found_exception

def retrive_farmer_productivity_record(validation_number: str, session: Session):
    statement = select(FarmerProductivityRecord).where(FarmerProductivityRecord.digitalId==validation_number)
    records = session.exec(statement).all()
    for record in records:
        session.refresh(record)
    return [FarmerProductivityRecordExpose(**record.model_dump()) for record in records]


@profile_router.get("/api/farmer/profile/{digitalId}",response_model=FarmerProfile)
def farmer_profile(token : Annotated[str,Depends(oauth2Scheme)],session: Session = Depends(get_session)):
    payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    user_type = "Farmer"
    validation_number = payload.get("vnum")
    user = get_user_detail(validation_number=validation_number,user_type=user_type,session=session)
    if user is None:
        raise user_not_found_exception
    user_profile = retrive_profile_info(validation_number=validation_number,user_type=user_type,session=session)
    if user_profile is None:
        raise user_profile_not_found_exception
    return user_profile

@profile_router.get("/api/loanshark/profile/{aadharCard}",response_model=LoanSharkProfile)
def loanshark_profile(token : Annotated[str,Depends(oauth2Scheme)],session: Session = Depends(get_session)):
    payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
    user_type = "LoanShark"
    validation_number = payload.get("vnum")
    user = get_user_detail(validation_number=validation_number,user_type=user_type,session=session)
    if user is None:
        raise user_not_found_exception
    user_profile = retrive_profile_info(validation_number=validation_number,user_type=user_type,session=session)
    if user_profile is None:
        raise user_profile_not_found_exception
    return user_profile

@profile_router.patch("/api/farmer/profile/edit/{digitalId}", response_model=FarmerProfile)
def edit_farmer_profile(digitalId: str, farmer_profile_update: FarmerProductivityRecordUpdate, token : Annotated[str,Depends(oauth2Scheme)], session: Session = Depends(get_session)):
    farmer = session.get(FarmerInDB,digitalId)
    if not farmer:
        raise user_not_found_exception
    update_dict = farmer_profile_update.model_dump(exclude_unset=True)
    productivity_updates = update_dict.pop("productivityRecords", None)

    for key,value in update_dict.items():
        setattr(farmer,key,value)

    if productivity_updates is not None:
        for record_update in productivity_updates:
            if record_update.month is None:
                continue
            statement = select(FarmerProductivityRecord).where(
                FarmerProductivityRecord.digitalId == digitalId,
                FarmerProductivityRecord.month == record_update.month
            )

            record = session.exec(statement).first()
            if record:
                for key,value in record_update.model_dump(exclude_unset=True).items():
                    setattr(record,key,value)
    session.commit()
    session.refresh(farmer)
    productivity_records = retrive_farmer_productivity_record(digitalId, session)
    profile_data = farmer.model_dump(exclude={"hashed_password", "aadharCard", "dob", "bankAccount"})
    profile_data["productivityRecords"] = productivity_records
    return FarmerProfile(**profile_data)

@profile_router.get("/api/lenders")
def fetch_all_lenders(token : Annotated[str,Depends(oauth2Scheme)], session: Session = Depends(get_session)):
    statement = select(LoanSharkInDB)
    all_profiles = session.exec(statement).all()
    post_processed_data = []
    for profile in all_profiles:
        post_processed_data.append(LoanSharkDashboard(**profile.model_dump()))
    return post_processed_data