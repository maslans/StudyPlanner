# Generated by Django 5.1.4 on 2025-01-09 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name subject'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(null=True, verbose_name='Term'),
        ),
        migrations.AlterField(
            model_name='task',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subject', verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('ASSIGNMENT', 'ASSIGNMENT'), ('EXAM', 'EXAM'), ('TEST', 'TEST')], max_length=20),
        ),
    ]