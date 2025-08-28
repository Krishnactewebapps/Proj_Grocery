from typing import Optional
from pydantic import BaseModel, Field, validator

class ProductModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    in_stock: int = Field(..., ge=0)
    category: Optional[str] = Field(None, max_length=50)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Sample Product",
                "description": "A sample product description.",
                "price": 19.99,
                "in_stock": 100,
                "category": "Electronics"
            }
        }

class ProductCreateModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    in_stock: int = Field(..., ge=0)
    category: Optional[str] = Field(None, max_length=50)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Product name must not be empty')
        return v

class ProductUpdateModel(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Product name must not be empty')
        return v
