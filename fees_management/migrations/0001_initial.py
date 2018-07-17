# Generated by Django 2.0 on 2018-07-15 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DpyFeeTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.FloatField()),
                ('cycle', models.IntegerField()),
                ('cycle_slot', models.IntegerField()),
                ('dsc', models.TextField()),
                ('mop', models.IntegerField(default=1)),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Dpy Payment Receipt',
                'db_table': 'dpy_fee_transaction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyFeeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=250)),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'dpy_fee_type',
                'db_table': 'dpy_fee_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteClassFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('cycle', models.PositiveSmallIntegerField()),
                ('display_name', models.CharField(max_length=250)),
                ('bifurcations', models.TextField(null=True)),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Institute Class Fee',
                'db_table': 'dpy_institute_class_fee',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DpyPaymentReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_or_chequeno', models.TextField(default=0, null=True)),
                ('response', models.TextField(default=0, null=True)),
                ('mop', models.IntegerField(default=4)),
                ('receipt_amount', models.FloatField()),
                ('status', models.PositiveSmallIntegerField()),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Dpy Payment Receipt',
                'db_table': 'dpy_payment_receipt',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DpyUserFeeIgnore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_discount', models.FloatField()),
                ('status', models.PositiveSmallIntegerField()),
                ('added_by', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('institute_class_fee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fees_management.DpyInstituteClassFee')),
            ],
            options={
                'verbose_name': 'Dpy User Fee Ignore',
                'db_table': 'dpy_user_fee_ignore',
                'managed': True,
            },
        ),
    ]
