# Generated by Django 5.1.5 on 2025-02-05 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispensing_operations_app', '0016_alter_order_oil_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
