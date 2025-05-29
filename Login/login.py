from Login import *
from ORM_Models import *

# ------ SQL MODELS/ PYDANTIC MODELS ------ #
 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    vnum: str

# ------ End OF All MODELS ------ #

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
login_router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

def verify_password(normal_password: str, hashed_password: str) -> bool:
    return pwdContext.verify(normal_password,hashed_password)

def generate_hash_password(normal_password: str):
    return pwdContext.hash(secret=normal_password)

def get_user_detail(validation_number: str, user_type: str, session: Session):
    if user_type=="Farmer":
        statement = select(FarmerInDB).where(FarmerInDB.digitalId==validation_number)
    elif user_type=="LoanShark":
        statement = select(LoanSharkInDB).where(LoanSharkInDB.aadharCard==validation_number)
    result = session.exec(statement).first()
    return result

def authenticate_user(validation_number: str, password: str, user_type: str, session: Session):
    user = get_user_detail(validation_number=validation_number, user_type=user_type, session=session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_jwt_token(data: dict):
    copied_data = data.copy()
    encoded_jwt = jwt.encode(copied_data,SECRET_KEY,ALGORITHM)
    return encoded_jwt

# ------ ENDPOINTS ------ #

@login_router.post("/api/farmer/login",response_model=Token)
def farmer_login(data: FarmerLogin, session: Session = Depends(get_session)) -> Token :
    user = authenticate_user(data.digitalId,data.password,"Farmer",session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(data={"vnum": data.digital_farmer_id})
    return {"access_token": access_token, "token_type": "bearer"}

@login_router.post("/api/loanshark/login",response_model=Token)
def loanshark_login(data: LoanSharkLogin, session: Session = Depends(get_session)) -> Token :
    user = authenticate_user(data.aadharCard,data.password,"LoanShark", session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(data={"vnum": data.aadharCard})
    return {"access_token": access_token, "token_type": "bearer"}

@login_router.post("/api/farmer/signup")
def farmer_signup(new_user_data: FarmerSignUP, session: Session = Depends(get_session)):
    statement = select(FarmerInDB).where(FarmerInDB.digitalId==new_user_data.digitalId)
    result = session.exec(statement).first()
    if result is not None:
        raise HTTPException(
        status_code=400,
        detail="Digital ID Number already registered",
        )
    hashed_password = generate_hash_password(new_user_data.password)
    farmer_new = FarmerInDB(
        name = new_user_data.name,
        aadharCard = new_user_data.aadharCard,
        digitalId = new_user_data.digitalId,
        dob = new_user_data.dob,
        bankAccount = new_user_data.bankAccount,
        hashed_password = hashed_password
    )
    session.add(farmer_new)
    session.commit()
    session.refresh(farmer_new)
    return farmer_new
    
@login_router.post("/api/loanshark/signup")
def loanshark_signup(new_user_data: LoanSharkSignUP, session: Session = Depends(get_session)):
    statement = select(LoanSharkInDB).where(LoanSharkInDB.aadharCard==new_user_data.aadharCard)
    result = session.exec(statement).first()
    if result is not None:
        raise HTTPException(
        status_code=400,
        detail="Aadhaar Number already registered",
        )
    hashed_password = generate_hash_password(new_user_data.password)
    loanshark_new = LoanSharkInDB(
        name = new_user_data.name,
        aadharCard = new_user_data.aadharCard,
        dob = new_user_data.dob,
        bankAccount = new_user_data.bankAccount,
        hashed_password = hashed_password
    )
    session.add(loanshark_new)
    session.commit()
    session.refresh(loanshark_new)
    return loanshark_new
    
@login_router.get("/api/userdetail")
def about_user(username: str, validation_number: str, user_type: str):
    return get_user_detail(username=username,validation_number=validation_number,user_type=user_type)