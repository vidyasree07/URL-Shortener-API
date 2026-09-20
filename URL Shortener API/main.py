from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
import time

app = FastAPI(title="URL Shortener API")

url_db = {}
analytics_db = {}

class URLRequest(BaseModel):
    url: str
    expiry_hours: int = 24

def generate_short_code(url: str) -> str:
    unique = url + str(time.time())
    return hashlib.md5(unique.encode()).hexdigest()[:6]

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = generate_short_code(request.url)
    url_db[short_code] = {
        "original_url": request.url,
        "created_at": time.time(),
        "expiry": time.time() + (request.expiry_hours * 3600)
    }
    analytics_db[short_code] = {"clicks": 0}
    return {
        "short_url": f"http://localhost:8000/{short_code}",
        "short_code": short_code,
        "expires_in_hours": request.expiry_hours
    }

@app.get("/analytics/{short_code}")
def get_analytics(short_code: str):
    if short_code not in analytics_db:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "short_code": short_code,
        "original_url": url_db[short_code]["original_url"],
        "total_clicks": analytics_db[short_code]["clicks"]
    }

@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code not in url_db:
        raise HTTPException(status_code=404, detail="URL not found")
    entry = url_db[short_code]
    if time.time() > entry["expiry"]:
        del url_db[short_code]
        raise HTTPException(status_code=410, detail="URL expired")
    analytics_db[short_code]["clicks"] += 1
    return RedirectResponse(url=entry["original_url"])

@app.get("/")
def root():
    return {"message": "URL Shortener API running!"}