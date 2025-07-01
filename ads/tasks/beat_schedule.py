from celery.schedules import crontab
from app.celery import app

app.conf.beat_schedule = {
    "toggle-campaigns-every-minute": {
        "task": "ads.tasks.campaign_toggle.toggle_campaigns_by_budget",
        "schedule": crontab(minute="*"),
    },
}
