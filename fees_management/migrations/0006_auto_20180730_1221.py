# Generated by Django 2.0 on 2018-07-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees_management', '0005_auto_20180730_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpypaymentreceipt',
            name='mop',
            field=models.IntegerField(default=2, null=True),
        ),
    ]
