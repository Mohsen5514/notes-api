# Notes API

A RESTful API built using Django and Django REST Framework.

## 🚀 Features

- JWT Authentication
- Pagination
- Throttling
- Caching
- Clean Architecture (Service Layer)
- Custom Exception Handling

## 🧠 Architecture

This project follows Clean Architecture principles:

- Views handle requests only
- Business logic lives inside a Service Layer
- Models handle data
- Serializers handle validation and transformation

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- SQLite (Development)

## 📂 Project Structure

- accounts/ → authentication logic
- tasks/ → notes application
- services.py → business logic layer

## ⚙️ How to Run

```bash
git clone <your-repo-url>
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver