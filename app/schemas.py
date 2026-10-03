from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field,field_validator
class ProfileIn(BaseModel):
    monthly_income:float=Field(ge=0); savings_goal:float=Field(ge=0)
class ProfileOut(ProfileIn):
    id:int; model_config=ConfigDict(from_attributes=True)
class ExpenseIn(BaseModel):
    title:str=Field(min_length=1,max_length=120); category:str=Field(min_length=1,max_length=50); amount:float=Field(gt=0); spent_at:datetime|None=None
    @field_validator("title","category")
    @classmethod
    def clean(cls,v):
        v=v.strip()
        if not v: raise ValueError("Value cannot be empty")
        return v
class ExpenseOut(ExpenseIn):
    id:int; spent_at:datetime; model_config=ConfigDict(from_attributes=True)
class AnalyzeOut(BaseModel):
    income:float; savings_goal:float; total_expenses:float; available_after_expenses:float; savings_gap:float; savings_progress_percent:float; category_totals:dict[str,float]; expense_count:int; budget_status:str; insights:list[str]
class RecommendationOut(BaseModel):
    source:str; recommendations:list[str]; summary:str
class ChatIn(BaseModel): message:str=Field(min_length=1,max_length=2000)
class ChatOut(BaseModel): reply:str; source:str
