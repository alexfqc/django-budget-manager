from celery import shared_task
from datetime import date
from ads.models import AdSpend

@shared_task
def generate_daily_spending_report() -> str:
    today = date.today()
    created_count = AdSpend.objects.filter(date=today).count()
    return f"{created_count} gastos gerados para {today}"
