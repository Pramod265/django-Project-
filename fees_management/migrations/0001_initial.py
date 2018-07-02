# Generated by Django 2.0 on 2018-07-02 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('class_user_profiling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DpyFeeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=250)),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'dpy_fee_type',
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteClassFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('cycle', models.PositiveSmallIntegerField()),
                ('display_name', models.CharField(max_length=250)),
                ('bifercations', models.CharField(max_length=255)),
                ('status', models.PositiveSmallIntegerField(verbose_name=1)),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.IntegerField(default=0)),
                ('fee_type_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fees_management.DpyFeeType')),
                ('institute_class_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='class_user_profiling.DpyInstituteClass')),
            ],
            options={
                'db_table': 'dpy_institute_class_fee',
            },
        ),
    ]
