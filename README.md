# Django Budget Manager

A campaign management system with daily and monthly budget control. This project uses Django and Celery to automatically activate or deactivate campaigns based on ad spend and allowed schedule (dayparting). Everything runs inside Docker — no need to install Python locally.

## 🧱 Tech Stack

- Python 3.11
- Django 5
- PostgreSQL 15
- Celery + Redis
- Docker + Docker Compose

## ⚙️ Requirements

- Docker
- Docker Compose

> No need to install Python, pip, poetry or any system dependencies.

## 🚀 How to Run the Project

Clone the repository and start the containers:

```bash
docker compose up --build
```

Open a new tab an run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create fake data:

```bash
docker compose exec web python manage.py seed_test_data
```
