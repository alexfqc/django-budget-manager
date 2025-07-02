from celery import shared_task
from datetime import date
from decimal import Decimal
from django.db.models import QuerySet
from django.db.models import Sum
from ads.models import Campaign, AdSpend, Brand


@shared_task
def reset_campaign_budgets() -> None:
    """
    Re-enables all campaigns at the start of a new day or month,
    assuming they are under their budget limits.
    """
    today: date = date.today()
    campaigns: QuerySet[Campaign] = Campaign.objects.all()
    reset_count: int = 0

    for campaign in campaigns:
        brand: Brand = campaign.brand

        daily_spent: Decimal = (
            AdSpend.objects
            .filter(campaign=campaign, date=today)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        monthly_spent: Decimal = (
            AdSpend.objects
            .filter(date__year=today.year, date__month=today.month, campaign=campaign)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        if (
            not campaign.is_active
            and daily_spent < brand.daily_budget
            and monthly_spent < brand.monthly_budget
        ):
            campaign.is_active = True
            campaign.save()
            reset_count += 1
            print(f"♻️ Campaign reactivated during budget reset: {campaign.name}")

    print(f"🔁 Budget reset complete — Reactivated campaigns: {reset_count}")
