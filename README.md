# URL Shortener API

REST API built with FastAPI that shortens URLs with analytics and expiry.

## Features
- Shorten any URL with unique 6-character code
- Click analytics tracking
- Auto-expiry after specified hours
- Redirect to original URL

## Tech Stack
Python, FastAPI, Uvicorn, Hashing

## Run
pip install -r requirements.txt
uvicorn main:app --reload

## API Endpoints
POST /shorten — shorten a URL
GET /{short_code} — redirect
GET /analytics/{short_code} — click stats
