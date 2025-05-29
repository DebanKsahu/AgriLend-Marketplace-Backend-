from ORM_Models.farmer_production_models import FarmerProductivityRecordExpose

def credit_utilization_ratio(curr_loan: float, loan_repaid: float) -> float:
    return (curr_loan/(curr_loan+loan_repaid))*100

def repayment_reliability_score(total_loan: float, loan_repaid: float) -> float:
    return (loan_repaid/total_loan)*100

def land_productivity_ratio(productivity_records: list[FarmerProductivityRecordExpose], farm_size: float) -> float:
    total_annual_yeild = sum([record.yield_value for record in productivity_records])
    return total_annual_yeild/farm_size

def loan_approval_rate(approved_application: int, total_application: int) -> float:
    return (approved_application/total_application)*100

def portfolio_yeild(total_earning: float, total_loan_portfolio_value: float) -> float:
    return (total_earning/total_loan_portfolio_value)*100

def loan_default_rate(no_of_defaulted_loans: int, loan_issued: int) -> float:
    return (no_of_defaulted_loans/loan_issued)*100

def operational_efficiency(operating_expense: float, total_income: float) -> float:
    return (operating_expense/total_income)*100