# Generated by Django 5.2.3 on 2025-06-29 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('daily_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_budget', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='ads.brand')),
            ],
        ),
        migrations.CreateModel(
            name='DaypartingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_hour', models.PositiveSmallIntegerField()),
                ('end_hour', models.PositiveSmallIntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dayparting', to='ads.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='AdSpend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spends', to='ads.campaign')),
            ],
            options={
                'unique_together': {('campaign', 'date')},
            },
        ),
    ]
