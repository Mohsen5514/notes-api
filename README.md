# Notes API

A RESTful API built with Django and Django REST Framework.

## Features
- JWT Authentication
- Pagination
- Throttling
- Caching
- Clean Architecture (Service Layer)
- Custom Exception Handling

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (dev)

## Project Structure
- accounts/ → authentication logic
- tasks/ → notes app
- services.py → business logic layer

## How to Run

```bash
git clone ...
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
