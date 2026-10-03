import os
os.environ['DATABASE_URL']='sqlite:///./data/test_pocketsmart.db'
from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        r=client.get('/api/health')
        assert r.status_code==200
        assert r.json()['status']=='ok'

def test_flow():
    with TestClient(app) as client:
        r=client.put('/api/profile',json={'monthly_income':30000,'savings_goal':8000})
        assert r.status_code==200
        r=client.post('/api/expenses',json={'title':'Lunch','category':'Food','amount':250})
        assert r.status_code==201
        e=r.json()['id']
        r=client.get('/api/analyze')
        assert r.status_code==200
        assert r.json()['category_totals']['Food']>=250
        r=client.delete(f'/api/expenses/{e}')
        assert r.status_code==200
