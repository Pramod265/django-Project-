# Generated by Django 2.0 on 2018-07-02 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpyinstitute',
            name='demo_link',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dpyinstitute',
            name='institute_website',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]