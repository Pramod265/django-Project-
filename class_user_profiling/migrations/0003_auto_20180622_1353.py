# Generated by Django 2.0.5 on 2018-06-22 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('class_user_profiling', '0002_auto_20180615_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='DpyInstituteClassSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_month', models.PositiveSmallIntegerField()),
                ('end_month', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('ic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='class_user_profiling.DpyInstituteClass')),
            ],
            options={
                'db_table': 'dpy_institute_class_session',
                'verbose_name': 'Institute Class Session',
            },
        ),
        migrations.RemoveField(
            model_name='dpyinstituteuserclass',
            name='ic',
        ),
        migrations.RemoveField(
            model_name='dpyinstituteuserclass',
            name='user',
        ),
        migrations.DeleteModel(
            name='DpyInstituteUserClass',
        ),
    ]
