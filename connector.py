from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx, os

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

async def proxy_get(path: str, params: dict = None):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BRIDGE_URL}{path}", params=params, headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

async def proxy_post(path: str, body: dict = None):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BRIDGE_URL}{path}", json=body, headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

async def proxy_patch(path: str, body: dict = None):
    async with httpx.AsyncClient() as client:
        r = await client.patch(f"{BRIDGE_URL}{path}", json=body, headers={"Authorization": BRIDGE_SECRET}, timeout=60)
        return r.json()

@app.get("/health")
async def health():
    return {"ok": True}

# ---------------------------
# Tickets
# ---------------------------
@app.get("/ticketsTopCompanies")
async def tickets_top_companies(days: int = Query(0), top: int = Query(5), pipeline: str = None, stage: str = None):
    return await proxy_get("/tickets/top-companies", {"days": days, "top": top, "pipeline": pipeline, "stage": stage})

@app.post("/ticketsSearch")
async def tickets_search(body: dict):
    return await proxy_post("/tickets/search", body)

@app.patch("/ticketsUpdate/{ticket_id}")
async def tickets_update(ticket_id: str, body: dict):
    return await proxy_patch(f"/tickets/update/{ticket_id}", body)

# ---------------------------
# Contacts
# ---------------------------
@app.get("/contactsGet/{contact_id}")
async def contacts_get(contact_id: str):
    return await proxy_get(f"/contacts/get/{contact_id}")

@app.post("/contactsUpsert")
async def contacts_upsert(body: dict):
    return await proxy_post("/contacts/upsert", body)

@app.post("/contactsSearch")
async def contacts_search(body: dict):
    return await proxy_post("/contacts/search", body)

# ---------------------------
# Companies
# ---------------------------
@app.get("/companiesGet/{company_id}")
async def companies_get(company_id: str):
    return await proxy_get(f"/companies/get/{company_id}")

@app.post("/companiesUpsert")
async def companies_upsert(body: dict):
    return await proxy_post("/companies/upsert", body)

@app.post("/companiesSearch")
async def companies_search(body: dict):
    return await proxy_post("/companies/search", body)

# ---------------------------
# Deals
# ---------------------------
@app.get("/dealsGet/{deal_id}")
async def deals_get(deal_id: str):
    return await proxy_get(f"/deals/get/{deal_id}")

@app.post("/dealsUpsert")
async def deals_upsert(body: dict):
    return await proxy_post("/deals/upsert", body)

@app.post("/dealsSearch")
async def deals_search(body: dict):
    return await proxy_post("/deals/search", body)

# ---------------------------
# Associations
# ---------------------------
@app.post("/associationsCreate")
async def associations_create(body: dict):
    return await proxy_post("/associations/create", body)

# ---------------------------
# Properties
# ---------------------------
@app.get("/propertiesList/{object_type}")
async def properties_list(object_type: str):
    return await proxy_get(f"/properties/list/{object_type}")

@app.post("/propertiesUpdate/{object_type}/{property_name}")
async def properties_update(object_type: str, property_name: str, body: dict):
    return await proxy_post(f"/properties/update/{object_type}/{property_name}", body)

# ---------------------------
# Workflows
# ---------------------------
@app.get("/workflowsList")
async def workflows_list():
    return await proxy_get("/workflows/list")

# ---------------------------
# Knowledge Base
# ---------------------------
@app.get("/kbArticlesList")
async def kb_articles_list(limit: int = Query(20), after: str = None):
    return await proxy_get("/kb/articles/list", {"limit": limit, "after": after})

@app.post("/kbArticlesCreate")
async def kb_articles_create(body: dict):
    return await proxy_post("/kb/articles/create", body)

# ---------------------------
# Schema
# ---------------------------
@app.get("/schema.json")
def schema():
    return JSONResponse({
        "openapi": "3.0.1",
        "info": {"title": "ChatGPT Connector", "version": "1.0.0"},
        "servers": [{"url": "https://hubspot-connector.onrender.com"}]
    })
