# Generated by Django 5.1.5 on 2025-01-16 11:44

import dispensing_operations_app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispensing_operations_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='status',
            new_name='Method',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='date',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.CharField(default=dispensing_operations_app.models.get_default_datetime, max_length=20),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dispensing_operations_app.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maintenance',
            name='created_at',
            field=models.CharField(default=dispensing_operations_app.models.get_default_datetime, max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.CharField(default=dispensing_operations_app.models.get_default_datetime, max_length=20),
        ),
        migrations.AddField(
            model_name='stock',
            name='created_at',
            field=models.CharField(default=dispensing_operations_app.models.get_default_datetime, max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.CharField(default=dispensing_operations_app.models.get_default_datetime, max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='created_at',
            field=models.CharField(default=dispensing_operations_app.models.get_default_datetime, max_length=20),
        ),
    ]
