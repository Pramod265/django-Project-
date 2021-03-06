# Generated by Django 2.0.5 on 2018-06-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0007_auto_20180530_0756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dpyinstituteusers',
            old_name='level',
            new_name='role',
        ),
        migrations.RemoveField(
            model_name='dpyinstituteusers',
            name='type',
        ),
        migrations.AddField(
            model_name='dpyinstitute',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='dpyinstitute',
            name='medium',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dpyusers',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='dpyinstitute',
            name='nature',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
