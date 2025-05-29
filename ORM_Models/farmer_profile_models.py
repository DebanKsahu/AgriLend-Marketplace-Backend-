from sqlmodel import SQLModel
from pydantic import model_validator
from typing import List
from ORM_Models.farmer_production_models import FarmerProductivityRecordExpose,FarmerProductivityRecordUpdate
from Math_Functions.functions import *

class FarmerProfile(SQLModel):
    name: str
    transactions: int = 0
    loans: float = 0.0
    loansRepaid: float = 0.0
    farmSize: float = 0.0
    productivityRecords: List[FarmerProductivityRecordExpose] = []
    creditUtilizationRatio: float = 0.0
    repaymentReliabilityScore: float = 0.0
    landProductivityRatio: float = 0.0

    @model_validator(mode="after")
    def compute_derived_values(self) -> "FarmerProfile":
        self.creditUtilizationRatio: float = credit_utilization_ratio(self.loans,self.loansRepaid)
        self.repaymentReliabilityScore: float = repayment_reliability_score(self.loans,self.loansRepaid)
        self.landProductivityRatio: float = land_productivity_ratio(self.productivityRecords,self.farmSize)
        return self

class FarmerProfileUpdate(SQLModel):
    name: str | None = None
    transactions: int | None = None
    loans: float | None = None
    loansRepaid: float | None = None
    farmSize: float | None = None
    productivityRecords: list[FarmerProductivityRecordUpdate] | None = None