# Product Management Documentation

## Overview
This document provides comprehensive documentation for the Product Management microservice, including workflows, API endpoints, business rules, logging, error handling, and a User Acceptance Testing (UAT) checklist.

---

## 1. Product Management Workflows

### 1.1. Add Product Workflow
- **Input:** Product details (name, description, price, in_stock, category)
- **Process:**
  1. Validate input data (e.g., name not empty, price > 0, in_stock >= 0).
  2. Insert product into MongoDB collection.
  3. Log the addition event.
  4. Return the created product.
- **Output:** Product object with assigned ID.

### 1.2. Update Product Workflow
- **Input:** Product ID, update fields (any subset of name, description, price, in_stock, category)
- **Process:**
  1. Validate update data (e.g., price > 0 if provided).
  2. Update product in MongoDB collection.
  3. Log the edit event.
  4. Return the updated product.
- **Output:** Updated product object.

### 1.3. List Products Workflow
- **Input:** Optional skip and limit parameters for pagination.
- **Process:**
  1. Fetch products from MongoDB with pagination.
  2. Return the list of products.
- **Output:** List of product objects.

### 1.4. Get Product Workflow
- **Input:** Product ID
- **Process:**
  1. Fetch product by ID from MongoDB.
  2. Return the product if found.
- **Output:** Product object or 404 error if not found.

---

## 2. API Endpoints

### 2.1. List Products
- **Endpoint:** `GET /products/`
- **Query Parameters:**
  - `skip` (int, optional): Number of items to skip (default: 0)
  - `limit` (int, optional): Max number of items to return (default: 100)
- **Response:** `200 OK` with list of products

### 2.2. Get Product by ID
- **Endpoint:** `GET /products/{product_id}`
- **Response:**
  - `200 OK` with product object
  - `404 Not Found` if product does not exist

### 2.3. Add Product
- **Endpoint:** `POST /products/`
- **Request Body:** ProductCreateModel
- **Response:**
  - `201 Created` with created product object
  - `400 Bad Request` for validation errors
  - `500 Internal Server Error` for server/database errors

### 2.4. Update Product
- **Endpoint:** `PUT /products/{product_id}`
- **Request Body:** ProductUpdateModel
- **Response:**
  - `200 OK` with updated product object
  - `400 Bad Request` if no update data provided
  - `404 Not Found` if product does not exist
  - `500 Internal Server Error` for server/database errors

---

## 3. Business Rules
- Product name must not be empty or whitespace.
- Product price must be greater than 0.
- Product in_stock must be zero or positive.
- Category is optional but, if provided, must not exceed 50 characters.
- On update, at least one field must be provided.
- All operations are logged for audit purposes.

---

## 4. Logging
- All product additions and edits are logged with timestamp, user, and details/changes.
- Logging is handled by the `LoggingService` using Python's `logging` module.
- Log format for addition: `[ADD] ProductID: <id> | User: <user> | Time: <timestamp> | Details: <dict>`
- Log format for edit: `[EDIT] ProductID: <id> | User: <user> | Time: <timestamp> | Changes: <dict>`
- Errors and warnings are logged with appropriate severity.

---

## 5. Error Handling
- All database and server errors return `500 Internal Server Error` with a generic message.
- Validation errors return `400 Bad Request` with details.
- Not found errors return `404 Not Found`.
- All errors are logged with stack trace and context.

---

## 6. UAT Checklist
- [ ] Can add a product with valid data and receive a 201 response.
- [ ] Cannot add a product with empty name or price <= 0 (400 error).
- [ ] Can update a product with valid fields and receive a 200 response.
- [ ] Cannot update a product with no fields (400 error).
- [ ] Cannot update a non-existent product (404 error).
- [ ] Can list products with pagination.
- [ ] Can fetch a product by ID.
- [ ] Cannot fetch a non-existent product (404 error).
- [ ] All add/edit actions are logged with correct format.
- [ ] All errors are logged and return appropriate HTTP status codes.
