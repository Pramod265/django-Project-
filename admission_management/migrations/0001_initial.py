# Generated by Django 2.0 on 2018-07-14 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DpyInstituteAdmissionProspect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email_id', models.EmailField(max_length=100, null='true')),
                ('phone_no', models.CharField(max_length=100, null='true')),
                ('gender', models.CharField(max_length=20)),
                ('course_id', models.CharField(max_length=100, null='true')),
                ('admission_status', models.PositiveSmallIntegerField(default=0)),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('institute_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='onboarding.DpyInstitute')),
            ],
            options={
                'db_table': 'dpy_institute_admissions_prospect',
            },
        ),
    ]
