# Generated by Django 2.0.5 on 2018-07-13 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('class_user_profiling', '0003_auto_20180713_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='DpyInstituteClassUserPresenties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marked_by', models.IntegerField()),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.IntegerField(default=0)),
                ('css', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='class_user_profiling.DpyInstituteClassSessionSubject')),
                ('ic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='class_user_profiling.DpyInstituteClass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Class User Presenties',
                'db_table': 'dpy_institute_class_user_presenties',
            },
        ),
        migrations.AlterUniqueTogether(
            name='dpyinstituteuserclass',
            unique_together={('user', 'ic', 'user_type')},
        ),
    ]
