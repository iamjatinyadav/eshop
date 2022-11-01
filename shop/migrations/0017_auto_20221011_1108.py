# Generated by Django 3.1 on 2022-10-11 11:08

from django.db import migrations

def slug_generator(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    print(Product.objects.filter(slug=''), "null value")
    # while Product.objects.filter(slug__isnull=True).exists():
        # with transaction.atomic():
    for row in Product.objects.filter(slug=''):
        row.slug = row.name.replace(" ", "-")
        row.save()
class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20221011_1108'),
    ]

    operations = [
        migrations.RunPython(slug_generator),

    ]