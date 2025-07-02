from celery.schedules import crontab
from app.celery import app

app.conf.beat_schedule = {
    "toggle-campaigns-every-minute": {
        "task": "ads.tasks.campaign_toggle.toggle_campaigns_by_budget",
        "schedule": crontab(minute="*"),
    },
    "track-daily-spend-every-minute": {
        "task": "ads.tasks.spend_tracking.track_ad_spend",
        "schedule": crontab(minute="*"),
    },
    "reset-campaign-budgets-daily": {
        "task": "ads.tasks.budget_reset.reset_campaign_budgets",
        "schedule": crontab(minute="*"),  
    },
}
