from celery import shared_task
from datetime import date
from django.db import models
from django.db.models import QuerySet
from ads.models import Campaign, AdSpend


@shared_task
def toggle_campaigns_by_budget() -> None:
    """
    Disables campaigns that exceed their daily or monthly budgets.
    Re-enables campaigns that are within their budget limits.
    """
    today: date = date.today()
    campaigns: QuerySet[Campaign] = Campaign.objects.all()
    deactivated_count: int = 0
    reactivated_count: int = 0

    for campaign in campaigns:
        # Calculate today's spend
        daily_spent: float = (
            AdSpend.objects
            .filter(campaign=campaign, date=today)
            .aggregate(total=models.Sum("amount"))["total"] or 0.0
        )

        # Calculate this month's spend
        monthly_spent: float = (
            AdSpend.objects
            .filter(
                campaign=campaign,
                date__year=today.year,
                date__month=today.month
            )
            .aggregate(total=models.Sum("amount"))["total"] or 0.0
        )

        # Disable campaign if it exceeded any budget
        if (daily_spent >= campaign.brand.daily_budget or monthly_spent >= campaign.brand.monthly_budget) and campaign.is_active:
            campaign.is_active = False
            campaign.save()
            deactivated_count += 1
            print(f"⛔ Campaign deactivated: {campaign.name}")

        # Reactivate campaign if it is within budget
        elif (daily_spent < campaign.brand.daily_budget and monthly_spent < campaign.brand.monthly_budget) and not campaign.is_active:
            campaign.is_active = True
            campaign.save()
            reactivated_count += 1
            print(f"✅ Campaign reactivated: {campaign.name}")

    print(f"🔁 Campaigns updated — Deactivated: {deactivated_count}, Reactivated: {reactivated_count}")
