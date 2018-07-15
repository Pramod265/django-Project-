# Generated by Django 2.0 on 2018-07-15 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DpyInstituteAdmissionFeesPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.IntegerField()),
                ('applicant_id', models.IntegerField()),
                ('course_id', models.IntegerField()),
                ('admission_for', models.CharField(blank=True, db_column='Admission_for', max_length=75, null=True)),
                ('payu_trans_id', models.CharField(blank=True, max_length=255, null=True)),
                ('reg_no', models.CharField(max_length=10)),
                ('total_amount', models.FloatField()),
                ('discount', models.FloatField()),
                ('dsc', models.TextField()),
                ('status', models.PositiveIntegerField()),
                ('mode', models.PositiveIntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.PositiveIntegerField()),
                ('updated_on', models.DateTimeField()),
            ],
            options={
                'db_table': 'dpy_institute_admission_fees_payments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionFor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.PositiveIntegerField()),
                ('admission_for_id', models.PositiveIntegerField()),
                ('course_id', models.IntegerField()),
                ('seats_intake', models.IntegerField()),
                ('status', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.IntegerField()),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.IntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admission_for',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.PositiveIntegerField()),
                ('admissions_user_id', models.PositiveIntegerField()),
                ('payu_trans_id', models.CharField(blank=True, max_length=30, null=True)),
                ('reg_no', models.CharField(max_length=10)),
                ('total_amount', models.FloatField()),
                ('discount', models.FloatField()),
                ('status', models.IntegerField()),
                ('mode', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.IntegerField()),
                ('updated_on', models.DateTimeField()),
            ],
            options={
                'db_table': 'dpy_institute_admission_payments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.IntegerField()),
                ('dmk_classes_id', models.PositiveIntegerField(blank=True, null=True)),
                ('intake_capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('course_name', models.CharField(max_length=200)),
                ('course_desc', models.TextField()),
                ('subjects', models.TextField(blank=True, null=True)),
                ('fees', models.FloatField()),
                ('applicable_discount', models.IntegerField()),
                ('status', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.IntegerField()),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.IntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_courses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsDiscounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.PositiveIntegerField()),
                ('category_id', models.IntegerField()),
                ('discount_value', models.FloatField()),
                ('discount_type', models.IntegerField()),
                ('status', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.IntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_discounts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsProspect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email_id', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(max_length=20)),
                ('course_id', models.CharField(blank=True, max_length=100, null=True)),
                ('admission_status', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField()),
                ('created_on', models.DateTimeField()),
                ('created_by', models.IntegerField()),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.IntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_prospect',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsProspects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.IntegerField()),
                ('name', models.CharField(max_length=70)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11)),
                ('gender', models.IntegerField()),
                ('course_ids', models.CharField(max_length=50)),
                ('admission_status', models.IntegerField()),
                ('status', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.IntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_prospects',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.PositiveIntegerField()),
                ('institute_form_id', models.IntegerField(blank=True, null=True)),
                ('reg_no', models.CharField(blank=True, max_length=10, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('local_address', models.CharField(max_length=255)),
                ('permanent_address', models.CharField(max_length=255)),
                ('aadhar_no', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(max_length=70)),
                ('middle_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('fathers_name', models.CharField(max_length=70)),
                ('mothers_name', models.CharField(max_length=70)),
                ('dob', models.CharField(max_length=70)),
                ('applicant_email', models.CharField(max_length=70)),
                ('gender', models.IntegerField()),
                ('applicant_phone', models.CharField(max_length=11)),
                ('category_id', models.IntegerField()),
                ('course_id', models.IntegerField()),
                ('caste', models.CharField(max_length=70)),
                ('parent_phone', models.CharField(max_length=11)),
                ('parent_email', models.CharField(max_length=70)),
                ('parent_occupation', models.CharField(max_length=70)),
                ('annual_income', models.FloatField()),
                ('subject_content', models.TextField(blank=True, null=True)),
                ('form_content', models.TextField()),
                ('nationality', models.IntegerField()),
                ('status', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.IntegerField()),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.IntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsUsersHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_id', models.PositiveIntegerField()),
                ('reg_no', models.CharField(blank=True, max_length=10, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('local_address', models.CharField(max_length=255)),
                ('permanent_address', models.CharField(max_length=255)),
                ('aadhar_no', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('fathers_name', models.CharField(max_length=70)),
                ('mothers_name', models.CharField(max_length=70)),
                ('middle_name', models.CharField(max_length=70)),
                ('dob', models.DateField()),
                ('gender', models.IntegerField()),
                ('applicant_email', models.CharField(max_length=70)),
                ('applicant_phone', models.CharField(max_length=11)),
                ('category_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('caste', models.CharField(max_length=77)),
                ('parent_phone', models.CharField(max_length=15)),
                ('parent_email', models.CharField(max_length=70)),
                ('parent_occupation', models.CharField(max_length=70)),
                ('annual_income', models.FloatField()),
                ('subject_content', models.TextField(blank=True, null=True)),
                ('form_content', models.TextField(blank=True, null=True)),
                ('nationality', models.PositiveIntegerField()),
                ('status', models.PositiveIntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.PositiveIntegerField()),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_users_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteAdmissionsUsersQualifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.PositiveIntegerField()),
                ('user_id', models.PositiveIntegerField()),
                ('qualification_id', models.PositiveIntegerField()),
                ('status', models.IntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_admissions_users_qualifications',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DpyInstituteCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_id', models.PositiveIntegerField()),
                ('category_name', models.CharField(max_length=65)),
                ('category_desc', models.TextField()),
                ('status', models.PositiveIntegerField()),
                ('added_on', models.DateTimeField()),
                ('added_by', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'dpy_institute_category',
                'managed': False,
            },
        ),
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
            ],
            options={
                'db_table': 'dpy_institute_admissions_prospect',
            },
        ),
    ]
