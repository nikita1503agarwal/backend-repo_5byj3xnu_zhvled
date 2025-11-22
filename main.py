import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Collection

app = FastAPI(title="Minimal Apparel Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Store backend running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# API models for requests
class SearchQuery(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    feature: Optional[str] = None
    limit: int = 24

@app.post("/api/products/search")
def search_products(payload: SearchQuery):
    if db is None:
        # Fallback sample data if no DB configured
        sample = [
            {
                "name": "AIR Tech Tee",
                "slug": "air-tech-tee",
                "price": 990,
                "category": "Men",
                "features": ["AIRism"],
                "images": ["https://images.unsplash.com/photo-1520975916090-3105956dac38?w=1200&q=60&auto=format&fit=crop"]
            },
            {
                "name": "Ultra Light Down Jacket",
                "slug": "ultra-light-down-jacket",
                "price": 4990,
                "category": "Women",
                "features": ["Ultra Light Down"],
                "images": ["https://images.unsplash.com/photo-1503342217505-b0a15cf70489?w=1200&q=60&auto=format&fit=crop"]
            },
        ]
        return sample[: payload.limit]

    filter_dict = {}
    if payload.q:
        # Simple text search across fields
        filter_dict["$or"] = [
            {"name": {"$regex": payload.q, "$options": "i"}},
            {"description": {"$regex": payload.q, "$options": "i"}},
            {"tags": {"$regex": payload.q, "$options": "i"}},
        ]
    if payload.category:
        filter_dict["category"] = payload.category
    if payload.feature:
        filter_dict["features"] = payload.feature

    docs = get_documents("product", filter_dict, limit=payload.limit)
    # Convert ObjectId to string if present
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return docs

@app.get("/api/collections")
def list_collections(limit: int = 6):
    if db is None:
        return [
            {
                "title": "HEATTECH",
                "slug": "heattech",
                "banner": "https://images.unsplash.com/photo-1516257984-b1b4d707412e?w=1600&q=60&auto=format&fit=crop"
            },
            {
                "title": "AIRism",
                "slug": "airism",
                "banner": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1600&q=60&auto=format&fit=crop"
            },
        ][:limit]

    docs = get_documents("collection", {}, limit=limit)
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return docs

@app.post("/api/products")
def create_product(product: Product):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not configured")
    inserted_id = create_document("product", product)
    return {"id": inserted_id}

@app.post("/api/collections")
def create_collection(collection: Collection):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not configured")
    inserted_id = create_document("collection", collection)
    return {"id": inserted_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
