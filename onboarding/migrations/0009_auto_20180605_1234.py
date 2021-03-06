# Generated by Django 2.0.5 on 2018-06-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0008_auto_20180605_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpyinstitute',
            name='address',
            field=models.CharField(blank=True, max_length=110),
        ),
        migrations.AlterField(
            model_name='dpyinstitute',
            name='board',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='dpyinstitute',
            name='contact',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='dpyinstitute',
            name='institute_email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]
