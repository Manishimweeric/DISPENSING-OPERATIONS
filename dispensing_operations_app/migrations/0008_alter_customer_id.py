# Generated by Django 5.1.5 on 2025-01-26 23:03

import dispensing_operations_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispensing_operations_app', '0007_customer_status_customerdetail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.CharField(default=dispensing_operations_app.models.generate_random_id, editable=False, max_length=5, primary_key=True, serialize=False, unique=True),
        ),
    ]
