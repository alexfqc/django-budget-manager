from django.contrib import admin
from .models import Brand, Campaign, AdSpend, DaypartingSchedule


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "daily_budget", "monthly_budget")


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "is_active")
    list_filter = ("brand", "is_active")


@admin.register(AdSpend)
class AdSpendAdmin(admin.ModelAdmin):
    list_display = ("campaign", "date", "amount")
    list_filter = ("date",)


@admin.register(DaypartingSchedule)
class DaypartingScheduleAdmin(admin.ModelAdmin):
    list_display = ("campaign", "start_hour", "end_hour")
    list_filter = ("campaign",)