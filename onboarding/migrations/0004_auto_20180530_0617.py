# Generated by Django 2.0.5 on 2018-05-30 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0003_auto_20180530_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpyinstituteusers',
            name='date_of_joining',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='dpyinstituteusers',
            name='date_of_leaving',
            field=models.DateField(null=True),
        ),
    ]
