# Generated by Django 2.0.5 on 2018-06-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0009_auto_20180605_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpyinstitute',
            name='created_by',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dpyinstituteusers',
            name='date_of_joining',
            field=models.DateField(null=True),
        ),
    ]
