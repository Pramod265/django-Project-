# Generated by Django 2.0 on 2018-07-25 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fees_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dpyinstituteclassfee',
            name='fee_type',
        ),
        migrations.DeleteModel(
            name='DpyFeeType',
        ),
    ]