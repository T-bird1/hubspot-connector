from fastapi import FastAPI, Query
import httpx, os
from fastapi.openapi.utils import get_openapi

BRIDGE_URL = os.getenv("BRIDGE_URL")
BRIDGE_SECRET = os.getenv("BRIDGE_SECRET")

app = FastAPI(title="ChatGPT Connector")

@app.get("/top-companies")
async def top_companies(days: int = Query(0), top: int = Query(5)):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BRIDGE_URL}/tickets/top-companies",
            params={"days": days, "top": top},
            headers={"Authorization": BRIDGE_SECRET},
            timeout=60
        )
        return r.json()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://hubspot-connector.onrender.com"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

from fastapi.responses import JSONResponse

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
            "/top-companies": {
                "get": {
                    "operationId": "getTopCompanies",
                    "summary": "Top companies by ticket count",
                    "parameters": [
                        { "name": "days", "in": "query", "schema": { "type": "integer", "minimum": 0 }, "required": false },
                        { "name": "top",  "in": "query", "schema": { "type": "integer", "minimum": 1, "maximum": 50 }, "required": false }
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
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "apiKeyAuth": { "type": "apiKey", "in": "header", "name": "Authorization" }
            }
        },
        "security": [{ "apiKeyAuth": [] }]
    })
