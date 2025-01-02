# inventory_management_API

This is Django REST Frameork (DRF) API to manage inventory for a store where users can add, update, and delete inventory items, and view inventory levels.

# Inventory Management API

## Setup Instructions

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Run server: `python manage.py runserver`

## API Endpoints

- `/api/items/`: CRUD operations for inventory items
- `/api/categories/`: CRUD operations for categories
- `/api/token/`: Obtain JWT token
- `/api/token/refresh/`: Refresh JWT token

# search and order functionality
GET /api/items/?min_quantity=10
GET /api/items/?category_name=electronics
GET /api/items/?search=laptop
GET /api/items/?ordering=-quantity


## Features

- Add, update, delete inventory items
- Categorize inventory items
- Track stock levels
- Low stock alerts
  """
