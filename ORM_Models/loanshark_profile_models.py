from sqlmodel import SQLModel
from pydantic import model_validator
from Math_Functions.functions import *

class LoanSharkProfile(SQLModel):
    name: str
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
    loanApprovalRate: float = 0.0
    loanDefaultRate: float = 0.0
    portfolioYield: float = 0.0
    operationalEfficiency: float = 0.0

    @model_validator(mode="after")
    def compute_derived_values(self) -> "LoanSharkProfile":
        self.loanApprovalRate = loan_approval_rate(self.applicationsApproved,self.applicationsTotal)
        self.loanDefaultRate = loan_default_rate(self.loansDefaulted,self.loansIssued)
        self.portfolioYield = portfolio_yeild(self.totalIncome,self.portfolioValue)
        self.operationalEfficiency = operational_efficiency(self.operatingExpenses,self.totalIncome)
        return self


class LoanSharkProfileUpdate(SQLModel):
    name: str | None = None
    totalCapital: float | None = None
    avgLoanSize: float | None = None
    interestRate: float | None = None
    repaymentTermMonths: int | None = None
    acceptedCollateral: bool | None = None
    customerBaseSize: int | None = None
    applicationsApproved: int | None = None
    applicationsTotal: int | None = None
    loansDefaulted: float | None = None
    loansIssued: float | None = None
    interestFees: float | None = None
    portfolioValue: float | None = None
    operatingExpenses: float | None = None
    totalIncome: float | None = None
