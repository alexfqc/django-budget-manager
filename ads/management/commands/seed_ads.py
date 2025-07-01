from typing import Any
from django.core.management.base import BaseCommand
from ads.models import Brand, Campaign, AdSpend, DaypartingSchedule
from django.utils import timezone
from decimal import Decimal
from random import randint, uniform
from datetime import date, timedelta


class Command(BaseCommand):
    help: str = "Seed the database with fake ad data"

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(self.style.WARNING("Clearing old data..."))
        DaypartingSchedule.objects.all().delete()
        AdSpend.objects.all().delete()
        Campaign.objects.all().delete()
        Brand.objects.all().delete()

        self.stdout.write("Creating brands, campaigns and ad spends...")

        for b in range(10):
            daily_budget: Decimal = Decimal(randint(100, 300))
            monthly_budget: Decimal = Decimal(randint(3000, 6000))
            brand: Brand = Brand.objects.create(
                name=f"Brand {b+1}",
                daily_budget=daily_budget,
                monthly_budget=monthly_budget,
            )

            for c in range(3):
                campaign_name: str = f"{brand.name} - Campaign {c+1}"
                campaign: Campaign = Campaign.objects.create(
                    brand=brand,
                    name=campaign_name,
                    is_active=True,
                )

                start_hour: int = randint(6, 10)
                end_hour: int = randint(17, 23)
                DaypartingSchedule.objects.create(
                    campaign=campaign,
                    start_hour=start_hour,
                    end_hour=end_hour,
                )

                for days_ago in range(30):
                    ad_date: date = timezone.now().date() - timedelta(days=days_ago)
                    amount: Decimal = Decimal(round(uniform(20.0, 150.0), 2))
                    AdSpend.objects.create(
                        campaign=campaign,
                        date=ad_date,
                        amount=amount,
                    )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded with test data!"))
