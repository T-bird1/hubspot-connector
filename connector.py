from fastapi import FastAPI, Query
import httpx, os

BRIDGE_URL = os.getenv("BRIDGE_URL")  # e.g. https://hubspot-bridge.onrender.com
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
