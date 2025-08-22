from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx, os, json

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

# ------------------------
# Tickets
# ------------------------
@app.get("/ticketsTopCompanies")
async def tickets_top_companies(days: int = Query(0), top: int = Query(5), pipeline: str = None, stage: str = None):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/tickets/top-companies",
            params={"days": days, "top": top, "pipeline": pipeline, "stage": stage},
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.post("/ticketsSearch")
async def tickets_search(body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/tickets/search",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.patch("/ticketsUpdate/{ticket_id}")
async def tickets_update(ticket_id: str, body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{BRIDGE_URL}/tickets/update/{ticket_id}",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Contacts
# ------------------------
@app.get("/contactsGet/{contact_id}")
async def contacts_get(contact_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/contacts/get/{contact_id}",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.post("/contactsUpsert")
async def contacts_upsert(body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/contacts/upsert",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Companies
# ------------------------
@app.get("/companiesGet/{company_id}")
async def companies_get(company_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/companies/get/{company_id}",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.post("/companiesUpsert")
async def companies_upsert(body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/companies/upsert",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Deals
# ------------------------
@app.get("/dealsGet/{deal_id}")
async def deals_get(deal_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/deals/get/{deal_id}",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.post("/dealsUpsert")
async def deals_upsert(body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/deals/upsert",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Associations
# ------------------------
@app.post("/associationsCreate")
async def associations_create(body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/associations/create",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Properties
# ------------------------
@app.get("/propertiesList/{object_type}")
async def properties_list(object_type: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/properties/list/{object_type}",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.post("/propertiesUpdate/{object_type}/{property_name}")
async def properties_update(object_type: str, property_name: str, body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/properties/update/{object_type}/{property_name}",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Workflows
# ------------------------
@app.get("/workflowsList")
async def workflows_list():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/workflows/list",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Knowledge Base
# ------------------------
@app.get("/kbArticlesList")
async def kb_articles_list(limit: int = Query(20), after: str = None):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/kb/articles/list",
            params={"limit": limit, "after": after},
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.post("/kbArticlesCreate")
async def kb_articles_create(body: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BRIDGE_URL}/kb/articles/create",
            json=body,
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Learner
# ------------------------
@app.get("/learningSuggestions")
async def learning_suggestions():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{os.getenv('LEARNER_URL')}/learning/suggestions",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.get("/learningKbCandidates")
async def learning_kb_candidates():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{os.getenv('LEARNER_URL')}/learning/kb-candidates",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ------------------------
# Serve External Schema
# ------------------------
@app.get("/schema.json")
def schema():
    with open("schema.json", "r") as f:
        schema_data = json.load(f)
    return JSONResponse(schema_data)
