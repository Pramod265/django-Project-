# Generated by Django 2.0 on 2018-07-14 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpyusers',
            name='gender',
            field=models.CharField(blank=True, choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Other')], max_length=20, null=True),
        ),
    ]
