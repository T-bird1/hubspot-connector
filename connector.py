from fastapi import FastAPI, Query, Path, Body
from fastapi.responses import JSONResponse
import httpx, os
from typing import List, Optional, Dict, Any

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector (Full)")

# ---------------------------
# Health Check
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------------------
# Tickets
# ---------------------------
@app.get("/tickets/top-companies")
async def tickets_top_companies(
    days: int = Query(0, ge=0),
    top: int = Query(5, ge=1, le=50),
    pipeline: Optional[str] = Query(None),
    stage: Optional[str] = Query(None)
):
    params = {"days": days, "top": top}
    if pipeline: params["pipeline"] = pipeline
    if stage: params["stage"] = stage
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/tickets/top-companies", params=params,
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/tickets/search")
async def tickets_search(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/tickets/search", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.patch("/tickets/update/{ticket_id}")
async def tickets_update(ticket_id: str = Path(...), properties: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.patch(f"{BRIDGE_URL}/tickets/update/{ticket_id}", json=properties,
                               headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Contacts
# ---------------------------
@app.get("/contacts/get/{contact_id}")
async def contacts_get(contact_id: str = Path(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/contacts/get/{contact_id}",
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/contacts/upsert")
async def contacts_upsert(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/contacts/upsert", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/contacts/search")
async def contacts_search(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/contacts/search", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Companies
# ---------------------------
@app.get("/companies/get/{company_id}")
async def companies_get(company_id: str = Path(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/companies/get/{company_id}",
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/companies/upsert")
async def companies_upsert(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/companies/upsert", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/companies/search")
async def companies_search(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/companies/search", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Deals
# ---------------------------
@app.get("/deals/get/{deal_id}")
async def deals_get(deal_id: str = Path(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/deals/get/{deal_id}",
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/deals/upsert")
async def deals_upsert(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/deals/upsert", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/deals/search")
async def deals_search(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/deals/search", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Associations
# ---------------------------
@app.post("/associations/create")
async def associations_create(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/associations/create", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Properties
# ---------------------------
@app.get("/properties/list/{object_type}")
async def properties_list(object_type: str = Path(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/properties/list/{object_type}",
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/properties/update/{object_type}/{property_name}")
async def properties_update(object_type: str = Path(...), property_name: str = Path(...), body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/properties/update/{object_type}/{property_name}", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Workflows
# ---------------------------
@app.get("/workflows/list")
async def workflows_list():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/workflows/list",
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Knowledge Base
# ---------------------------
@app.get("/kb/articles/list")
async def kb_articles_list(limit: int = Query(20, ge=1, le=100), after: Optional[str] = Query(None)):
    params = {"limit": limit}
    if after:
        params["after"] = after
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}/kb/articles/list", params=params,
                             headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.post("/kb/articles/create")
async def kb_articles_create(body: Dict[str, Any] = Body(...)):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}/kb/articles/create", json=body,
                              headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

# ---------------------------
# Static Schema
# ---------------------------
@app.get("/schema.json")
def schema():
    return JSONResponse({
        "openapi": "3.0.1",
        "info": {"title": "ChatGPT Connector (Full)", "version": "1.0.0"},
        "servers": [
            {"url": "https://hubspot-connector.onrender.com"},
            {"url": "https://hubspot-connector.onrender.com/"}
        ],
        "paths": {
            "/health": {"get": {"operationId": "health"}},
            "/tickets/top-companies": {"get": {"operationId": "ticketsTopCompanies"}},
            "/tickets/search": {"post": {"operationId": "ticketsSearch"}},
            "/tickets/update/{ticket_id}": {"patch": {"operationId": "ticketsUpdate"}},
            "/contacts/get/{contact_id}": {"get": {"operationId": "contactsGet"}},
            "/contacts/upsert": {"post": {"operationId": "contactsUpsert"}},
            "/contacts/search": {"post": {"operationId": "contactsSearch"}},
            "/companies/get/{company_id}": {"get": {"operationId": "companiesGet"}},
            "/companies/upsert": {"post": {"operationId": "companiesUpsert"}},
            "/companies/search": {"post": {"operationId": "companiesSearch"}},
            "/deals/get/{deal_id}": {"get": {"operationId": "dealsGet"}},
            "/deals/upsert": {"post": {"operationId": "dealsUpsert"}},
            "/deals/search": {"post": {"operationId": "dealsSearch"}},
            "/associations/create": {"post": {"operationId": "associationsCreate"}},
            "/properties/list/{object_type}": {"get": {"operationId": "propertiesList"}},
            "/properties/update/{object_type}/{property_name}": {"post": {"operationId": "propertiesUpdate"}},
            "/workflows/list": {"get": {"operationId": "workflowsList"}},
            "/kb/articles/list": {"get": {"operationId": "kbArticlesList"}},
            "/kb/articles/create": {"post": {"operationId": "kbArticlesCreate"}},
        }
    })
