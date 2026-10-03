import csv,io
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from fastapi import Depends,FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import Base,engine,get_db
from .models import Expense
from .schemas import AnalyzeOut,ChatIn,ChatOut,ExpenseIn,ExpenseOut,ProfileIn,ProfileOut,RecommendationOut
from .services.budget import analyze,get_expenses,get_profile
from .services.gemini import chat,generate_recommendations
@asynccontextmanager
async def lifespan(app):
    Path("data").mkdir(exist_ok=True);Base.metadata.create_all(bind=engine);yield
app=FastAPI(title="PocketSmart AI",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
STATIC=Path(__file__).parent/"static";app.mount("/static",StaticFiles(directory=STATIC),name="static")
@app.get("/",include_in_schema=False)
def index():return FileResponse(STATIC/"index.html")
@app.get("/api/health")
def health():return {"status":"ok","service":"PocketSmart AI"}
@app.get("/api/profile",response_model=ProfileOut)
def profile(db:Session=Depends(get_db)):return get_profile(db)
@app.put("/api/profile",response_model=ProfileOut)
def update_profile(payload:ProfileIn,db:Session=Depends(get_db)):
    p=get_profile(db);p.monthly_income=payload.monthly_income;p.savings_goal=payload.savings_goal;db.commit();db.refresh(p);return p
@app.get("/api/expenses",response_model=list[ExpenseOut])
def expenses(db:Session=Depends(get_db)):return get_expenses(db)
@app.post("/api/expenses",response_model=ExpenseOut,status_code=201)
def add_expense(payload:ExpenseIn,db:Session=Depends(get_db)):
    e=Expense(title=payload.title,category=payload.category,amount=payload.amount,spent_at=payload.spent_at or datetime.utcnow());db.add(e);db.commit();db.refresh(e);return e
@app.put("/api/expenses/{expense_id}",response_model=ExpenseOut)
def edit_expense(expense_id:int,payload:ExpenseIn,db:Session=Depends(get_db)):
    e=db.get(Expense,expense_id)
    if not e:raise HTTPException(404,"Expense not found")
    e.title=payload.title;e.category=payload.category;e.amount=payload.amount
    if payload.spent_at:e.spent_at=payload.spent_at
    db.commit();db.refresh(e);return e
@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id:int,db:Session=Depends(get_db)):
    e=db.get(Expense,expense_id)
    if not e:raise HTTPException(404,"Expense not found")
    db.delete(e);db.commit();return {"message":"Expense deleted"}
@app.get("/api/analyze",response_model=AnalyzeOut)
def analysis(db:Session=Depends(get_db)):return analyze(db)
@app.get("/api/recommendations",response_model=RecommendationOut)
def recommendations(db:Session=Depends(get_db)):
    d=analyze(db);source,recs=generate_recommendations(d);return {"source":source,"recommendations":recs,"summary":f"Budget status: {d['budget_status']}"}
@app.post("/api/chat",response_model=ChatOut)
def assistant_chat(payload:ChatIn,db:Session=Depends(get_db)):
    reply,source=chat(payload.message,analyze(db));return {"reply":reply,"source":source}
@app.get("/api/export.csv",include_in_schema=False)
def export_csv(db:Session=Depends(get_db)):
    buf=io.StringIO();w=csv.writer(buf);w.writerow(["id","title","category","amount","spent_at"])
    for e in get_expenses(db):w.writerow([e.id,e.title,e.category,f"{e.amount:.2f}",e.spent_at.isoformat()])
    return StreamingResponse(iter([buf.getvalue()]),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=pocketsmart-expenses.csv"})
