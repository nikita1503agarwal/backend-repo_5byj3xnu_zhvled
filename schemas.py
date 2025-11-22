"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Brand/user example remains for reference
class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    name: str = Field(..., description="Product display name")
    slug: str = Field(..., description="URL-friendly unique identifier")
    description: Optional[str] = Field(None, description="Product description")
    category: str = Field(..., description="Primary category, e.g., Women/Men/Kids/Baby")
    subcategory: Optional[str] = Field(None, description="Subcategory, e.g., Tops, Bottoms")
    price: float = Field(..., ge=0, description="Price in INR")
    colors: List[str] = Field(default_factory=list, description="Available color names")
    sizes: List[str] = Field(default_factory=list, description="Available sizes")
    materials: List[str] = Field(default_factory=list, description="Materials/fabrics")
    features: List[str] = Field(default_factory=list, description="Technical features like HEATTECH, AIRism")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    stock: int = Field(0, ge=0, description="Total stock across variants")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")
    tags: List[str] = Field(default_factory=list, description="Search tags")
    meta: Dict[str, str] = Field(default_factory=dict, description="Extra meta info like care, fit")

class Collection(BaseModel):
    """
    Collections schema
    Collection name: "collection"
    """
    title: str = Field(..., description="Collection title")
    slug: str = Field(..., description="URL-friendly unique identifier")
    description: Optional[str] = Field(None, description="Collection description")
    banner: Optional[str] = Field(None, description="Banner image URL")
    productIds: List[str] = Field(default_factory=list, description="Product slugs included in this collection")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
