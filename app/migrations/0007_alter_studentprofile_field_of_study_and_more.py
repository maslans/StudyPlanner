# Generated by Django 5.1.4 on 2025-01-11 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_subject_name_alter_task_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='field_of_study',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.fieldofstudy', verbose_name='Field Of Study'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.university', verbose_name='School'),
        ),
    ]
