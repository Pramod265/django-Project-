# Generated by Django 2.0 on 2018-07-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees_management', '0006_auto_20180730_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpypaymentreceipt',
            name='mop',
            field=models.IntegerField(null=True),
        ),
    ]
