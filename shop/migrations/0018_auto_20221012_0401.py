# Generated by Django 3.1 on 2022-10-12 04:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20221011_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e6ba6fd9-ffc1-414c-97a9-971b21718c94'), editable=False, primary_key=True, serialize=False),
        ),
    ]
