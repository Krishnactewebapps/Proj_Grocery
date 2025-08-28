import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.models.product import ProductModel, ProductCreateModel, ProductUpdateModel
from app.services.product_service import ProductService
from app.services.logging_service import LoggingService

# Fixtures for test data
def sample_product_dict():
    return {
        "_id": "507f1f77bcf86cd799439011",
        "name": "Test Product",
        "description": "A test product.",
        "price": 10.0,
        "in_stock": 5,
        "category": "TestCat"
    }

def sample_product_create():
    return ProductCreateModel(
        name="Test Product",
        description="A test product.",
        price=10.0,
        in_stock=5,
        category="TestCat"
    )

def sample_product_update():
    return ProductUpdateModel(
        name="Updated Product",
        price=12.5
    )

def test_add_product_success():
    collection = MagicMock()
    collection.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
    service = ProductService(collection)
    product_data = sample_product_create()
    with patch("app.services.product_service.ProductModel", autospec=True) as MockProductModel:
        MockProductModel.return_value = "product_model_instance"
        result = service.add_product(product_data)
        assert result == "product_model_instance"
        collection.insert_one.assert_called_once()

def test_add_product_db_error():
    collection = MagicMock()
    collection.insert_one.side_effect = Exception("DB error")
    service = ProductService(collection)
    product_data = sample_product_create()
    with pytest.raises(HTTPException) as exc:
        service.add_product(product_data)
    assert exc.value.status_code == 500

def test_update_product_success():
    collection = MagicMock()
    collection.update_one.return_value.matched_count = 1
    service = ProductService(collection)
    update_data = sample_product_update()
    with patch.object(service, 'get_product', return_value="updated_product") as mock_get:
        result = service.update_product("507f1f77bcf86cd799439011", update_data)
        assert result == "updated_product"
        collection.update_one.assert_called_once()
        mock_get.assert_called_once()

def test_update_product_not_found():
    collection = MagicMock()
    collection.update_one.return_value.matched_count = 0
    service = ProductService(collection)
    update_data = sample_product_update()
    result = service.update_product("507f1f77bcf86cd799439011", update_data)
    assert result is None

def test_update_product_no_data():
    collection = MagicMock()
    service = ProductService(collection)
    update_data = ProductUpdateModel()
    with pytest.raises(HTTPException) as exc:
        service.update_product("507f1f77bcf86cd799439011", update_data)
    assert exc.value.status_code == 400

def test_logging_addition_and_edit(monkeypatch):
    logging_service = LoggingService()
    logs = []
    monkeypatch.setattr(logging_service.logger, "info", lambda msg: logs.append(msg))
    # Test addition log
    logging_service.log_product_addition("507f1f77bcf86cd799439011", "tester", {"foo": "bar"})
    assert any("[ADD] ProductID: 507f1f77bcf86cd799439011" in log for log in logs)
    # Test edit log
    logging_service.log_product_edit("507f1f77bcf86cd799439011", "tester", {"baz": "qux"})
    assert any("[EDIT] ProductID: 507f1f77bcf86cd799439011" in log for log in logs)

def test_data_consistency_on_add_and_update():
    collection = MagicMock()
    # Simulate insert_one and update_one
    collection.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
    collection.update_one.return_value.matched_count = 1
    # Simulate find_one for get_product
    collection.find_one.return_value = sample_product_dict()
    service = ProductService(collection)
    # Add product
    product_data = sample_product_create()
    with patch("app.services.product_service.ProductModel", autospec=True) as MockProductModel:
        MockProductModel.return_value = "product_model_instance"
        added = service.add_product(product_data)
        assert added == "product_model_instance"
    # Update product
    update_data = sample_product_update()
    with patch("app.services.product_service.ProductModel", autospec=True) as MockProductModel:
        MockProductModel.return_value = "updated_product_model_instance"
        updated = service.update_product("507f1f77bcf86cd799439011", update_data)
        assert updated == "updated_product_model_instance"
    # Data consistency: get_product returns correct data
    with patch("app.services.product_service.ProductModel", autospec=True) as MockProductModel:
        MockProductModel.return_value = "product_model_instance"
        product = service.get_product("507f1f77bcf86cd799439011")
        assert product == "product_model_instance"
