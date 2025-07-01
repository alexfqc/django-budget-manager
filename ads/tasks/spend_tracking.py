import random
from celery import shared_task
from datetime import date
from ads.models import Campaign, AdSpend


@shared_task
def track_ad_spend() -> None:
    today = date.today()
    created_count = 0
    updated_count = 0

    active_campaigns = Campaign.objects.filter(is_active=True)
    if not active_campaigns:
        print("No campaigns are currently active.")
        return
    for campaign in active_campaigns:
        # Simulate a random amount spent for the day
        amount_spent = round(random.uniform(20.0, 200.0), 2)

        _, created = AdSpend.objects.update_or_create(
            campaign=campaign,
            date=today,
            defaults={"amount": amount_spent},
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

        print(f"[{campaign.name}] Gasto do dia: R${amount_spent}")

    print(f"✅ {created_count} registros criados, {updated_count} atualizados.")
