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

### Create the .env file at root folder and add this code:

```bash
POSTGRES_DB=budget_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DJANGO_SECRET_KEY=your-secret
POSTGRES_PORT=5432
DEBUG=True
POSTGRES_HOST=db
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### Open your terminal, go to your project folder and run

```bash
docker compose up --build
```

### Open a new tab an run migrations:

```bash
docker compose exec web python manage.py migrate
```

### Create fake data:

```bash
docker compose exec web python manage.py seed_test_data
```

### Go back to first tab where you ran:

```bash
docker compose up --build
```

And you'll be able to see celery logs with schedule tasks:

```bash
celery-1       | [2025-07-02 12:30:00,030: WARNING/ForkPoolWorker-8] ⏰ Activated: Campaign 1-1
celery-1       | [2025-07-02 12:30:00,031: WARNING/ForkPoolWorker-8] ⏰ Activated: Campaign 3-1
celery-1       | [2025-07-02 12:30:00,032: WARNING/ForkPoolWorker-8] 🌙 Deactivated: Campaign 3-2
celery-1       | [2025-07-02 12:30:00,032: WARNING/ForkPoolWorker-8] 🕒 Dayparting update — Activated: 2, Deactivated: 1
celery-1       | [2025-07-02 12:30:00,033: WARNING/ForkPoolWorker-9] [Campaign 2-1] Daily spend: $82.08
celery-1       | [2025-07-02 12:30:00,034: WARNING/ForkPoolWorker-9] [Campaign 3-2] Daily spend: $62.07
celery-1       | [2025-07-02 12:30:00,034: WARNING/ForkPoolWorker-9] ✅ 0 records created, 2 updated.
celery-1       | [2025-07-02 12:30:00,036: WARNING/ForkPoolWorker-2] ⛔ Campaign deactivated: Campaign 2-1
celery-1       | [2025-07-02 12:30:00,039: INFO/ForkPoolWorker-8] Task ads.tasks.dayparting.enforce_dayparting_rules[8dd6f6f0-0f6a-4987-9d87-4f9b72b49c00] succeeded in 0.018098291999876892s: None
celery-1       | [2025-07-02 12:30:00,040: INFO/ForkPoolWorker-9] Task ads.tasks.spend_tracking.track_ad_spend[768657f4-19b4-4026-86bf-7551fe76ad93] succeeded in 0.017054542000096262s: None
celery-1       | [2025-07-02 12:30:00,040: WARNING/ForkPoolWorker-1] 🔁 Budget reset complete — Reactivated campaigns: 0
celery-1       | [2025-07-02 12:30:00,043: WARNING/ForkPoolWorker-2] ⛔ Campaign deactivated: Campaign 1-1
celery-1       | [2025-07-02 12:30:00,043: WARNING/ForkPoolWorker-2] 🔁 Campaigns updated — Deactivated: 2, Reactivated: 0
```

## Notes

For propose of testing tasks were schedule to run every minute, but they could be scheduled to run once a day (hour=0, minute=0)
