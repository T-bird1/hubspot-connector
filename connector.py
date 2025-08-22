from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx, os
from typing import List, Optional

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

# ---------------------------
# Tickets Top Companies
# ---------------------------
@app.get("/ticketsTopCompanies")
async def tickets_top_companies(
    days: int = Query(0, ge=0),
    top: int = Query(5, ge=1, le=50),
    pipeline: Optional[str] = Query(None),
    stage: Optional[str] = Query(None)
):
    params = {"days": days, "top": top}
    if pipeline:
        params["pipeline"] = pipeline
    if stage:
        params["stage"] = stage

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/tickets/top-companies",
            params=params,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ---------------------------
# Tickets Search
# ---------------------------
@app.get("/ticketsSearch")
async def tickets_search(
    limit: int = Query(5, ge=1, le=100),
    after: Optional[str] = Query(None),
    properties: Optional[List[str]] = Query(None),
    associations: Optional[List[str]] = Query(None)
):
    params = {"limit": limit}
    if after:
        params["after"] = after
    if properties:
        params["properties"] = properties
    if associations:
        params["associations"] = associations

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/tickets/search",
            params=params,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ---------------------------
# Static OpenAPI schema
# ---------------------------
@app.get("/schema.json")
def schema():
    return JSONResponse({
        "openapi": "3.0.1",
        "info": {"title": "ChatGPT Connector", "version": "1.0.0"},
        "servers": [
            {"url": "https://hubspot-connector.onrender.com"},
            {"url": "https://hubspot-connector.onrender.com/"}
        ],
        "paths": {
            "/ticketsTopCompanies": {
                "get": {
                    "operationId": "ticketsTopCompanies",
                    "summary": "Top companies by ticket count",
                    "parameters": [
                        {"name": "days", "in": "query", "schema": {"type": "integer", "minimum": 0}, "required": False},
                        {"name": "top", "in"
