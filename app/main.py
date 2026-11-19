"""AI Sourcing Copilot demo HTTP API. NOT production ready."""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .matcher import CATALOG, parse_requirements, match

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"demo_rfq.sqlite3"
app=FastAPI(title="AI Sourcing Copilot Demo API",version="0.1.0",
            description="Rule-based sample catalog. No AI inference, live suppliers or actual pricing.")

def conn():
    c=sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS rfqs (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT NOT NULL)")
    return c

class RequirementText(BaseModel):
    text:str=Field(min_length=1,max_length=5000)

class MatchRequest(BaseModel):
    text:str=""
    interface:str="any"
    shutter:str="any"
    os:str="any"
    arch:str="any"
    min_mp:float=Field(default=0,ge=0,le=1000)
    min_fps:int=Field(default=0,ge=0,le=100000)
    max_price:float|None=Field(default=None,ge=0)
    qty:int=Field(default=1,ge=1,le=100000)

class RFQ(BaseModel):
    sku:str
    requirements:dict
    qty:int=Field(ge=1,le=100000)
    destination:str=Field(min_length=2,max_length=150)
    notes:str=Field(default="",max_length=3000)

@app.get("/")
def home():
    return FileResponse(ROOT/"AI采购选型_在线演示单文件.html",media_type="text/html")

@app.get("/api/health")
def health():
    return {"ok":True,"mode":"synthetic rule-based demo","live_data":False}

@app.get("/api/products")
def products():
    return {"items":CATALOG,"synthetic":True}

@app.post("/api/parse")
def parse(data:RequirementText):
    return {"requirements":parse_requirements(data.text),"method":"regex demonstration (not LLM)"}

@app.post("/api/match")
def matching(data:MatchRequest):
    try:
        return match(data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

@app.post("/api/rfqs",status_code=201)
def create_rfq(data:RFQ):
    if data.sku not in {p["sku"] for p in CATALOG}:
        raise HTTPException(status_code=422,detail="Unknown demo SKU")
    rid="DRFQ-"+uuid.uuid4().hex[:8].upper()
    record={"id":rid,"created_at":datetime.now(timezone.utc).isoformat(),
            "status":"draft-only","demo":True,**data.model_dump()}
    with conn() as c:
        c.execute("INSERT INTO rfqs(id,created_at,payload) VALUES(?,?,?)",
                  (rid,record["created_at"],json.dumps(record,ensure_ascii=False)))
    return record

@app.get("/api/rfqs")
def rfqs():
    with conn() as c:
        rows=c.execute("SELECT payload FROM rfqs ORDER BY created_at DESC LIMIT 100").fetchall()
    return {"items":[json.loads(row[0]) for row in rows],"demo":True}
