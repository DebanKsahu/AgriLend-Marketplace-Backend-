from sqlmodel import Field, SQLModel
from datetime import date
class FarmerBase(SQLModel):
    digitalId: str = Field(primary_key=True,index=True)

class FarmerLogin(FarmerBase):
    password: str 

class FarmerSignUP(FarmerLogin):
    name: str
    aadharCard: str
    dob: date
    bankAccount: str 

class FarmerInDB(FarmerBase,table=True):
    name: str
    aadharCard: str = Field(index=True) 
    dob: date
    bankAccount: str
    transactions: int = 0
    loans: float = 0.0
    loansRepaid: float = 0.0
    farmSize: float = 0.0
    hashed_password: str

class LoanSharkBase(SQLModel):
    aadharCard: str = Field(primary_key=True,index=True)

class LoanSharkLogin(LoanSharkBase):
    password: str 

class LoanSharkSignUP(LoanSharkLogin):
    name: str
    dob: date
    bankAccount: str 

class LoanSharkInDB(LoanSharkBase,table=True):
    name: str
    loansharkLogo: str = ""
    dob: date
    bankAccount: str
    hashed_password: str
    totalCapital: float = 0.0
    avgLoanSize: float = 0.0
    interestRate: float = 0.0
    repaymentTermMonths: int = 0
    acceptedCollateral: bool = True
    customerBaseSize: int = 0
    applicationsApproved: int = 0
    applicationsTotal: int = 0
    loansDefaulted: float = 0.0
    loansIssued: float = 0.0
    interestFees: float = 0.0
    portfolioValue: float = 0.0
    operatingExpenses: float = 0.0
    totalIncome: float = 0.0