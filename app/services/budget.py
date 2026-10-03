from collections import defaultdict
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import BudgetProfile,Expense
DEFAULT_PROFILE_ID=1
def get_profile(db:Session):
    p=db.get(BudgetProfile,DEFAULT_PROFILE_ID)
    if p is None:
        p=BudgetProfile(id=1,monthly_income=0,savings_goal=0);db.add(p);db.commit();db.refresh(p)
    return p
def get_expenses(db:Session): return list(db.scalars(select(Expense).order_by(Expense.spent_at.desc(),Expense.id.desc())).all())
def analyze(db:Session):
    p=get_profile(db); ex=get_expenses(db); total=round(sum(x.amount for x in ex),2); income=round(p.monthly_income,2); goal=round(p.savings_goal,2); available=round(income-total,2); gap=round(max(goal-available,0),2); progress=round(max(available,0)/goal*100,1) if goal else 0
    cats=defaultdict(float)
    for x in ex: cats[x.category]+=x.amount
    cats={k:round(v,2) for k,v in sorted(cats.items(),key=lambda z:z[1],reverse=True)}
    if income==0: status="Set your income"
    elif total>income: status="Over budget"
    elif goal and available<goal: status="Savings goal at risk"
    elif total>income*.7: status="High spending"
    else: status="On track"
    insights=[]
    if not ex: insights.append("No expenses have been recorded yet.")
    if income and total>income*.5: insights.append("More than half of the monthly income has already been spent.")
    if cats:
        top=next(iter(cats));insights.append(f"Your largest expense category is {top} at ₹{cats[top]:,.2f}.")
    if goal and available<goal: insights.append(f"You need about ₹{gap:,.2f} more available to reach the savings goal.")
    if available>=goal and goal: insights.append("The current recorded spending leaves enough for the savings goal.")
    return dict(income=income,savings_goal=goal,total_expenses=total,available_after_expenses=available,savings_gap=gap,savings_progress_percent=min(progress,100),category_totals=cats,expense_count=len(ex),budget_status=status,insights=insights)
