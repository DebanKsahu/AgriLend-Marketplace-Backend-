from sqlmodel import SQLModel,Field,Relationship,Column
from sqlalchemy.dialects.mysql import JSON
from typing import List
from enum import Enum
from pydantic import model_validator
from datetime import datetime,date,timezone
import uuid

class Status(str,Enum):
    PENDING = "Pending"
    UNDER_REVIEW = "Under Review"
    DOCUMENT_REQ = "Documents Required"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class Event(str,Enum):
    APPLICATION_SUBMITTED = "Application Submitted"
    INITIAL_REVIEW = "Initial Review"
    CREDIT_CHECK = "Credit Check"
    FARM_INSPECTION = "Farm Inspection"
    LOAN_APPROVED = "Loan Approved"
    ADDITIONAL_DOC = "Additional Documents Requested"
    DECLINATION = "Application Declined"


class LoanTimeLineEvent(SQLModel):
    date: date
    event: Event
    status: Status

    @classmethod
    def initial_submission(cls, curr_status: Status = Status.APPROVED):
        return cls(date=date.today(), event=Event.APPLICATION_SUBMITTED, status=curr_status)
    
class LoanTimeLineEventsInDB(SQLModel,table=True):
    eventId: int | None = Field(default=None,primary_key=True)
    loanInfoId: str = Field(foreign_key="loaninfoindb.id")
    date: date
    event: Event
    status: Status

class LoanInfoInDB(SQLModel,table=True):
    id: str = Field(default_factory=lambda : str(uuid.uuid4()), primary_key=True)
    aadhaarId: str = Field(foreign_key="loansharkindb.aadharCard")
    farmerId: str = Field(foreign_key="farmerindb.digitalId")
    loanAmount: float
    loanTermMonth: int
    requestedInterestRate: float
    purpose: str
    status: Status 
    dateApplied: date = Field(default_factory=lambda: datetime.now(timezone.utc).date())
    lastUpdated: date = Field(default_factory=lambda: datetime.now(timezone.utc).date())
    progress: float = 0.0
    documents: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    # timeline: List[LoanTimeLineEventsInDB] = Relationship(back_populates=None)

class LoanInfoCreate(SQLModel):
    aadhaarId: str 
    farmerId: str 
    loanAmount: float
    loanTermMonth: int
    requestedInterestRate: float
    purpose: str
    status: Status = Status.PENDING

class LoanInfoExposeToFarmer(SQLModel):
    id: str 
    lenderName: str
    lenderLogo: str
    loanAmount: float
    purpose: str
    status: Status 
    dateApplied: date
    lastUpdated: date
    requestedInterestRate: float | None
    loanTermMonth: int
    progress: float
    documents: List[str]
    timeline: List[LoanTimeLineEvent]

class LoanInfoExposeToLender(SQLModel):
    id: str 
    farmerName: str
    loanAmount: float
    purpose: str
    status: Status 
    dateApplied: date
    loanTermMonth: int