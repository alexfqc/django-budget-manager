from django.core.management.base import BaseCommand
from django.utils import timezone
from ads.models import Brand, Campaign, AdSpend, DaypartingSchedule
from django.db.models import Model
from datetime import datetime, timedelta, date
from typing import Any

class Command(BaseCommand):
    help: str = "Seed the database with test data for campaign scheduling."

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Deleting existing data...")
        AdSpend.objects.all().delete()
        DaypartingSchedule.objects.all().delete()
        Campaign.objects.all().delete()
        Brand.objects.all().delete()

        now: datetime = timezone.now()
        today: date = now.date()
        current_hour: int = now.hour

        self.stdout.write("Creating brands and campaigns...")

        for i in range(3):
            brand: Brand = Brand.objects.create(
                name=f"Brand {i+1}",
                daily_budget=50 + i * 25,       # 50, 75, 100
                monthly_budget=1000 + i * 500   # 1000, 1500, 2000
            )

            for j in range(2):
                campaign: Campaign = Campaign.objects.create(
                    brand=brand,
                    name=f"Campaign {i+1}-{j+1}",
                    is_active=True
                )

                spent_today: float = (
                    float(brand.daily_budget)
                    if j == 0 else float(brand.daily_budget) - 5
                )

                AdSpend.objects.create(
                    campaign=campaign,
                    date=today,
                    amount=spent_today
                )

                hour_offset: int = 0 if j == 0 else 1
                start_hour: int = (current_hour + hour_offset) % 24
                end_hour: int = (start_hour + 1) % 24

                DaypartingSchedule.objects.create(
                    campaign=campaign,
                    start_hour=start_hour,
                    end_hour=end_hour
                )

        self.stdout.write(self.style.SUCCESS("✅ Test data successfully created."))
