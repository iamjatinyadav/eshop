# Generated by Django 3.1 on 2022-11-03 07:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20221103_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.product'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ac36282b-6646-418d-ad87-c0bc42c7fdab'), editable=False, primary_key=True, serialize=False),
        ),
    ]
