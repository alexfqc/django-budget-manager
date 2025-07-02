from celery import shared_task
from datetime import datetime
from django.db.models import QuerySet
from ads.models import Campaign, DaypartingSchedule


@shared_task
def enforce_dayparting_rules() -> None:
    """
    Activates or deactivates campaigns based on their dayparting schedule.
    """
    now: datetime = datetime.now()
    current_hour: int = now.hour

    schedules: QuerySet[DaypartingSchedule] = DaypartingSchedule.objects.select_related("campaign")
    activated: int = 0
    deactivated: int = 0

    for schedule in schedules:
        campaign: Campaign = schedule.campaign
        within_schedule: bool = schedule.start_hour <= current_hour < schedule.end_hour

        if within_schedule and not campaign.is_active:
            campaign.is_active = True
            campaign.save()
            activated += 1
            print(f"⏰ Activated: {campaign.name}")

        elif not within_schedule and campaign.is_active:
            campaign.is_active = False
            campaign.save()
            deactivated += 1
            print(f"🌙 Deactivated: {campaign.name}")

    print(f"🕒 Dayparting update — Activated: {activated}, Deactivated: {deactivated}")
