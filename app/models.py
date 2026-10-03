from datetime import datetime
from sqlalchemy import DateTime,Float,Integer,String
from sqlalchemy.orm import Mapped,mapped_column
from .database import Base
class BudgetProfile(Base):
    __tablename__="budget_profiles"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,default=1)
    monthly_income:Mapped[float]=mapped_column(Float,default=0)
    savings_goal:Mapped[float]=mapped_column(Float,default=0)
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class Expense(Base):
    __tablename__="expenses"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    title:Mapped[str]=mapped_column(String(120))
    category:Mapped[str]=mapped_column(String(50),index=True)
    amount:Mapped[float]=mapped_column(Float)
    spent_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
