import logging
from typing import List, Optional
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson import ObjectId
from fastapi import HTTPException
from app.models.product import ProductModel, ProductCreateModel, ProductUpdateModel

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_product(self, product_id: str) -> Optional[ProductModel]:
        try:
            product = self.collection.find_one({"_id": ObjectId(product_id)})
            if not product:
                logger.warning(f"Product with id {product_id} not found.")
                return None
            return ProductModel(**product)
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_products(self, skip: int = 0, limit: int = 100) -> List[ProductModel]:
        try:
            products = self.collection.find().skip(skip).limit(limit)
            return [ProductModel(**prod) for prod in products]
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def add_product(self, product_data: ProductCreateModel) -> ProductModel:
        try:
            product_dict = product_data.dict(exclude_unset=True)
            result = self.collection.insert_one(product_dict)
            product_dict["_id"] = result.inserted_id
            logger.info(f"Product added with id {result.inserted_id}")
            return ProductModel(**product_dict)
        except PyMongoError as e:
            logger.error(f"Database error adding product: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update_product(self, product_id: str, update_data: ProductUpdateModel) -> Optional[ProductModel]:
        try:
            update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
            if not update_dict:
                logger.warning(f"No update data provided for product {product_id}")
                raise HTTPException(status_code=400, detail="No update data provided")
            result = self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_dict})
            if result.matched_count == 0:
                logger.warning(f"Product with id {product_id} not found for update.")
                return None
            logger.info(f"Product {product_id} updated.")
            return self.get_product(product_id)
        except PyMongoError as e:
            logger.error(f"Database error updating product: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def propagate_product_update(self, product_id: str):
        # Placeholder for propagation logic (e.g., notify other services, send events, etc.)
        try:
            logger.info(f"Propagating update for product {product_id}")
            # Implement actual propagation logic here
        except Exception as e:
            logger.error(f"Error propagating product update for {product_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
