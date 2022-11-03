# Generated by Django 3.1 on 2022-11-03 09:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20221103_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='total_price',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bc618e44-4371-4d89-9a97-d5a3a0d8ffda'), editable=False, primary_key=True, serialize=False),
        ),
    ]
