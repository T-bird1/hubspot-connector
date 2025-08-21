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
