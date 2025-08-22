import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx, os, json

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

# ------------------------
# Helper: retry with backoff
# ------------------------
async def fetch_with_retries(url, method="GET", params=None, body=None, max_retries=5):
    backoff = 1  # start at 1 second
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            if method == "GET":
                r = await client.get(
                    url,
                    params=params,
                    headers={"Authorization": BRIDGE_SECRET},
                    timeout=60
                )
            elif method == "POST":
                r = await client.post(
                    url,
                    json=body,
                    headers={"Authorization": BRIDGE_SECRET},
                    timeout=60
                )
            elif method == "PATCH":
                r = await client.patch(
                    url,
                    json=body,
                    headers={"Authorization": BRIDGE_SECRET},
                    timeout=60
                )
            else:
                raise ValueError(f"Unsupported method {method}")

            # If not rate limited → return result
            if r.status_code != 429:
                return r.json()

            # Rate limited → wait and retry
            retry_after = int(r.headers.get("Retry-After", backoff))
            await asyncio.sleep(retry_after)
            backoff *= 2  # exponential backoff

        # Too many retries
        return {"error": "Rate limit exceeded after retries"}

# ------------------------
# Tickets
# ------------------------
@app.get("/ticketsTopCompanies")
async def tickets_top_companies(days: int = Query(0), top: int = Query(5), pipeline: str = None, stage: str = None):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/tickets/top-companies",
        method="GET",
        params={"days": days, "top": top, "pipeline": pipeline, "stage": stage}
    )

@app.post("/ticketsSearch")
async def tickets_search(body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/tickets/search",
        method="POST",
        body=body
    )

@app.patch("/ticketsUpdate/{ticket_id}")
async def tickets_update(ticket_id: str, body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/tickets/update/{ticket_id}",
        method="PATCH",
        body=body
    )

# ------------------------
# Contacts
# ------------------------
@app.get("/contactsGet/{contact_id}")
async def contacts_get(contact_id: str):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/contacts/get/{contact_id}",
        method="GET"
    )

@app.post("/contactsUpsert")
async def contacts_upsert(body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/contacts/upsert",
        method="POST",
        body=body
    )

# ------------------------
# Companies
# ------------------------
@app.get("/companiesGet/{company_id}")
async def companies_get(company_id: str):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/companies/get/{company_id}",
        method="GET"
    )

@app.post("/companiesUpsert")
async def companies_upsert(body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/companies/upsert",
        method="POST",
        body=body
    )

# ------------------------
# Deals
# ------------------------
@app.get("/dealsGet/{deal_id}")
async def deals_get(deal_id: str):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/deals/get/{deal_id}",
        method="GET"
    )

@app.post("/dealsUpsert")
async def deals_upsert(body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/deals/upsert",
        method="POST",
        body=body
    )

# ------------------------
# Associations
# ------------------------
@app.post("/associationsCreate")
async def associations_create(body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/associations/create",
        method="POST",
        body=body
    )

# ------------------------
# Properties
# ------------------------
@app.get("/propertiesList/{object_type}")
async def properties_list(object_type: str):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/properties/list/{object_type}",
        method="GET"
    )

@app.post("/propertiesUpdate/{object_type}/{property_name}")
async def properties_update(object_type: str, property_name: str, body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/properties/update/{object_type}/{property_name}",
        method="POST",
        body=body
    )

# ------------------------
# Workflows
# ------------------------
@app.get("/workflowsList")
async def workflows_list():
    return await fetch_with_retries(
        f"{BRIDGE_URL}/workflows/list",
        method="GET"
    )

# ------------------------
# Knowledge Base
# ------------------------
@app.get("/kbArticlesList")
async def kb_articles_list(limit: int = Query(20), after: str = None):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/kb/articles/list",
        method="GET",
        params={"limit": limit, "after": after}
    )

@app.post("/kbArticlesCreate")
async def kb_articles_create(body: dict):
    return await fetch_with_retries(
        f"{BRIDGE_URL}/kb/articles/create",
        method="POST",
        body=body
    )

# ------------------------
# Learner
# ------------------------
@app.get("/learningSuggestions")
async def learning_suggestions():
    return await fetch_with_retries(
        f"{os.getenv('LEARNER_URL')}/learning/suggestions",
        method="GET"
    )

@app.get("/learningKbCandidates")
async def learning_kb_candidates():
    return await fetch_with_retries(
        f"{os.getenv('LEARNER_URL')}/learning/kb-candidates",
        method="GET"
    )

# ------------------------
# Serve External Schema
# ------------------------
@app.get("/schema.json")
def schema():
    # Always serve the patched static-schema.json so ChatGPT gets correct mappings
    with open("static-schema.json", "r") as f:
        schema_data = json.load(f)
    return JSONResponse(schema_data)
