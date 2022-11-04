# Generated by Django 3.1 on 2022-11-03 10:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20221103_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d53646ca-fd7b-4070-a78b-efd977af4e31'), editable=False, primary_key=True, serialize=False),
        ),
    ]