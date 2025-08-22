from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx, os

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

# ---------------------------
# Tickets Top Companies
# ---------------------------
@app.get("/ticketsTopCompanies")
async def tickets_top_companies(days: int = Query(0), top: int = Query(5)):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/tickets/top-companies",
            params={"days": days, "top": top},
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

# ---------------------------
# Tickets Search
# ---------------------------
@app.get("/ticketsSearch")
async def tickets_search(limit: int = Query(5)):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/tickets/search",
            params={"limit": limit},
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
        "info": { "title": "ChatGPT Connector", "version": "1.0.0" },
        "servers": [
            { "url": "https://hubspot-connector.onrender.com" },
            { "url": "https://hubspot-connector.onrender.com/" }
        ],
        "paths": {
            "/ticketsTopCompanies": {
                "get": {
                    "operationId": "ticketsTopCompanies",
                    "summary": "Top companies by ticket count",
                    "parameters": [
                        { "name": "days", "in": "query", "schema": { "type": "integer", "minimum": 0 }, "required": False },
                        { "name": "top",  "in": "query", "schema": { "type": "integer", "minimum": 1, "maximum": 50 }, "required": False }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "items": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "rank": { "type": "integer" },
                                                        "companyId": { "type": "string" },
                                                        "companyName": { "type": "string" },
                                                        "ticketCount": { "type": "integer" }
                                                    },
                                                    "required": ["rank","companyId","ticketCount"]
                                                }
                                            },
                                            "total_tickets": { "type": "integer" }
                                        },
                                        "required": ["total_tickets"]
                                    }
                                }
                            }
                        }
                    },
                    "security": [{ "apiKeyAuth": [] }]
                }
            },
            "/ticketsSearch": {
                "get": {
                    "operationId": "ticketsSearch",
                    "summary": "Search tickets",
                    "parameters": [
                        { "name": "limit", "in": "query", "schema": { "type": "integer", "minimum": 1, "maximum": 100 }, "required": False }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    },
                    "security": [{ "apiKeyAuth": [] }]
                }
            }
        },
        "components": {
            "securitySchemes": {
                "apiKeyAuth": { "type": "apiKey", "in": "header", "name": "Authorization" }
            }
        }
    })
