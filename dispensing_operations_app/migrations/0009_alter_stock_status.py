# Generated by Django 5.1.5 on 2025-01-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispensing_operations_app', '0008_alter_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='status',
            field=models.CharField(default='In Stock', max_length=50),
        ),
    ]
