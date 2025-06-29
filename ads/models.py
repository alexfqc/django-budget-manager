# Create your models here.
from django.db import models
from django.utils import timezone
from typing import Optional


class Brand(models.Model):
    name: str = models.CharField(max_length=100)
    daily_budget: float = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_budget: float = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Campaign(models.Model):
    brand: Brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="campaigns")
    name: str = models.CharField(max_length=100)
    is_active: bool = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class AdSpend(models.Model):
    campaign: Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="spends")
    date: timezone.datetime = models.DateField()
    amount: float = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("campaign", "date")

    def __str__(self) -> str:
        return f"{self.campaign.name} - {self.date} - ${self.amount}"


class DaypartingSchedule(models.Model):
    campaign: Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="dayparting")
    start_hour: int = models.PositiveSmallIntegerField()
    end_hour: int = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.campaign.name}: {self.start_hour}h–{self.end_hour}h"
