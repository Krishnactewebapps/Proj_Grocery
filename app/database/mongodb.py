import logging
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson import ObjectId
from app.models.product import ProductModel, ProductCreateModel, ProductUpdateModel

logger = logging.getLogger(__name__)

class MongoDBClient:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection: Collection = self.db[collection_name]
            logger.info(f"Connected to MongoDB database: {db_name}, collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_product(self, product_id: str) -> Optional[ProductModel]:
        try:
            product = self.collection.find_one({"_id": ObjectId(product_id)})
            if not product:
                logger.warning(f"Product with id {product_id} not found.")
                return None
            return ProductModel(**product)
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {e}")
            return None

    def get_products(self, skip: int = 0, limit: int = 100) -> List[ProductModel]:
        try:
            products = self.collection.find().skip(skip).limit(limit)
            return [ProductModel(**prod) for prod in products]
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []

    def add_product(self, product_data: ProductCreateModel) -> Optional[ProductModel]:
        try:
            product_dict = product_data.dict(exclude_unset=True)
            result = self.collection.insert_one(product_dict)
            product_dict["_id"] = result.inserted_id
            logger.info(f"Product added with id {result.inserted_id}")
            return ProductModel(**product_dict)
        except PyMongoError as e:
            logger.error(f"Database error adding product: {e}")
            return None
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            return None

    def update_product(self, product_id: str, update_data: ProductUpdateModel) -> Optional[ProductModel]:
        try:
            update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
            if not update_dict:
                logger.warning(f"No update data provided for product {product_id}")
                return None
            result = self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_dict})
            if result.matched_count == 0:
                logger.warning(f"Product with id {product_id} not found for update.")
                return None
            logger.info(f"Product {product_id} updated.")
            return self.get_product(product_id)
        except PyMongoError as e:
            logger.error(f"Database error updating product: {e}")
            return None
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            return None

    def delete_product(self, product_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(product_id)})
            if result.deleted_count == 1:
                logger.info(f"Product {product_id} deleted.")
                return True
            else:
                logger.warning(f"Product {product_id} not found for deletion.")
                return False
        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            return False
