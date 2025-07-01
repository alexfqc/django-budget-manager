from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class AdSpend(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="spends")
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("campaign", "date")

    def __str__(self) -> str:
        return f"{self.campaign.name} - {self.date} - ${self.amount}"


class DaypartingSchedule(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="dayparting")
    start_hour = models.PositiveSmallIntegerField()
    end_hour = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.campaign.name}: {self.start_hour}h–{self.end_hour}h"
