# Generated by Django 2.0 on 2018-06-22 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0004_auto_20180622_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpyusers',
            name='password',
            field=models.CharField(default=123, max_length=128),
        ),
    ]