from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx, os

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

# ------------------------
# Proxy Endpoints
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

@app.get("/workflowsList")
async def workflows_list():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/workflows/list",
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

@app.get("/kbArticlesList")
async def kb_articles_list(limit: int = Query(20), after: str = None):
    async with httpx.AsyncClient() as client:
        params = {"limit": limit}
        if after:
            params["after"] = after
        r = await client.get(
            f"{BRIDGE_URL}/kb/articles/list",
            params=params,
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
# Schema for GPT Actions
# ------------------------

@app.get("/schema.json")
def schema():
    schema = {
        "openapi": "3.1.0",
        "info": {"title": "HubSpot Connector", "version": "1.0.0"},
        "servers": [
            {"url": "https://hubspot-connector.onrender.com"},
            {"url": "https://hubspot-connector.onrender.com/"}
        ],
        "paths": {
            # Tickets
            "/ticketsTopCompanies": {
                "get": {
                    "operationId": "ticketsTopCompanies",
                    "summary": "Top companies by ticket count",
                    "parameters": [
                        {"name": "days", "in": "query", "schema": {"type": "integer", "minimum": 0}, "required": False},
                        {"name": "top", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 50}, "required": False},
                        {"name": "pipeline", "in": "query", "schema": {"type": "string"}, "required": False},
                        {"name": "stage", "in": "query", "schema": {"type": "string"}, "required": False}
                    ],
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/ticketsSearch": {
                "post": {
                    "operationId": "ticketsSearch",
                    "summary": "Search tickets",
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/ticketsUpdate/{ticket_id}": {
                "patch": {
                    "operationId": "ticketsUpdate",
                    "summary": "Update a ticket's properties",
                    "parameters": [
                        {"name": "ticket_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # Contacts
            "/contactsGet/{contact_id}": {
                "get": {
                    "operationId": "contactsGet",
                    "summary": "Get a contact",
                    "parameters": [
                        {"name": "contact_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/contactsUpsert": {
                "post": {
                    "operationId": "contactsUpsert",
                    "summary": "Upsert contact by email",
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # Companies
            "/companiesGet/{company_id}": {
                "get": {
                    "operationId": "companiesGet",
                    "summary": "Get a company",
                    "parameters": [
                        {"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/companiesUpsert": {
                "post": {
                    "operationId": "companiesUpsert",
                    "summary": "Upsert company by domain",
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # Deals
            "/dealsGet/{deal_id}": {
                "get": {
                    "operationId": "dealsGet",
                    "summary": "Get a deal",
                    "parameters": [
                        {"name": "deal_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/dealsUpsert": {
                "post": {
                    "operationId": "dealsUpsert",
                    "summary": "Upsert deal by name",
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # Associations
            "/associationsCreate": {
                "post": {
                    "operationId": "associationsCreate",
                    "summary": "Create association between objects",
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # Properties
            "/propertiesList/{object_type}": {
                "get": {
                    "operationId": "propertiesList",
                    "summary": "List properties for object type",
                    "parameters": [
                        {"name": "object_type", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/propertiesUpdate/{object_type}/{property_name}": {
                "post": {
                    "operationId": "propertiesUpdate",
                    "summary": "Update a property definition",
                    "parameters": [
                        {"name": "object_type", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "property_name", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # Workflows
            "/workflowsList": {
                "get": {
                    "operationId": "workflowsList",
                    "summary": "List workflows",
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            # KB
            "/kbArticlesList": {
                "get": {
                    "operationId": "kbArticlesList",
                    "summary": "List knowledge base articles",
                    "parameters": [
                        {"name": "limit", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 100}, "required": False},
                        {"name": "after", "in": "query", "schema": {"type": "string"}, "required": False}
                    ],
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            },
            "/kbArticlesCreate": {
                "post": {
                    "operationId": "kbArticlesCreate",
                    "summary": "Create a knowledge base article",
                    "requestBody": {"required": True},
                    "responses": {"200": {"description": "OK"}},
                    "security": [{"apiKeyAuth": []}]
                }
            }
        },
        "components": {
            "securitySchemes": {
                "apiKeyAuth": {"type": "apiKey", "in": "header", "name": "Authorization"}
            }
        }
    }
    return JSONResponse(schema)
