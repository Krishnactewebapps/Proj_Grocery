from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.product import ProductModel, ProductCreateModel, ProductUpdateModel
from app.services.product_service import ProductService
from app.services.logging_service import LoggingService
from app.db.mongodb_client import get_product_collection
from pymongo.collection import Collection

router = APIRouter(prefix="/products", tags=["products"])

# Dependency to get ProductService instance
def get_product_service(collection: Collection = Depends(get_product_collection)):
    return ProductService(collection)

# Dependency to get LoggingService instance
def get_logging_service():
    return LoggingService()

@router.get("/", response_model=List[ProductModel])
def list_products(skip: int = 0, limit: int = 100, service: ProductService = Depends(get_product_service)):
    """Get a list of products."""
    return service.get_products(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductModel)
def get_product(product_id: str, service: ProductService = Depends(get_product_service)):
    """Get a single product by ID."""
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
def add_product(
    product: ProductCreateModel,
    service: ProductService = Depends(get_product_service),
    logger: LoggingService = Depends(get_logging_service),
    user: str = "system"  # In real app, get from auth
):
    """Add a new product."""
    new_product = service.add_product(product)
    logger.log_product_addition(str(new_product.id), user, new_product.dict())
    return new_product

@router.put("/{product_id}", response_model=ProductModel)
def update_product(
    product_id: str,
    update: ProductUpdateModel,
    service: ProductService = Depends(get_product_service),
    logger: LoggingService = Depends(get_logging_service),
    user: str = "system"  # In real app, get from auth
):
    """Update an existing product."""
    updated_product = service.update_product(product_id, update)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or no update data provided")
    logger.log_product_edit(product_id, user, update.dict(exclude_unset=True))
    return updated_product
