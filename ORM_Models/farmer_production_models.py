from sqlmodel import SQLModel,Field

class FarmerProductivityRecord(SQLModel,table=True):
    digitalId: str = Field(foreign_key="farmerindb.digitalId",primary_key=True)
    month: str 
    productivity: int
    yield_value: int 

class FarmerProductivityRecordExpose(SQLModel):
    month: str 
    productivity: int
    yield_value: int 

class FarmerProductivityRecordUpdate(SQLModel):
    month: str | None = None
    productivity: int | None = None
    yield_value: int | None = None