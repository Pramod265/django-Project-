# Generated by Django 2.0 on 2018-07-15 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fees_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('class_user_profiling', '0002_auto_20180715_0703'),
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpyuserfeeignore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dpypaymentreceipt',
            name='institute_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='onboarding.DpyInstitute'),
        ),
        migrations.AddField(
            model_name='dpyinstituteclassfee',
            name='fee_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fees_management.DpyFeeType'),
        ),
        migrations.AddField(
            model_name='dpyinstituteclassfee',
            name='institute_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='class_user_profiling.DpyInstituteClass'),
        ),
    ]