# Generated by Django 5.1.4 on 2025-01-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('TASK', 'TASK'), ('EXAM', 'EXAM'), ('TEST', 'TEST')], max_length=20),
        ),
    ]