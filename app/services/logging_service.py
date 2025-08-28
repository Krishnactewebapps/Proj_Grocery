import logging
from datetime import datetime
from typing import Optional

class LoggingService:
    def __init__(self):
        self.logger = logging.getLogger("product_audit")

    def log_product_addition(self, product_id: str, user: str, details: dict):
        timestamp = datetime.utcnow().isoformat()
        self.logger.info(f"[ADD] ProductID: {product_id} | User: {user} | Time: {timestamp} | Details: {details}")

    def log_product_edit(self, product_id: str, user: str, changes: dict):
        timestamp = datetime.utcnow().isoformat()
        self.logger.info(f"[EDIT] ProductID: {product_id} | User: {user} | Time: {timestamp} | Changes: {changes}")
