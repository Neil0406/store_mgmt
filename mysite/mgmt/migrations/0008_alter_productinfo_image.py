# Generated by Django 3.2.2 on 2021-05-14 14:47

from django.db import migrations, models
import mgmt.utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('mgmt', '0007_productinfo_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=mgmt.utils.storage.ImageStorage(), upload_to='./static/product_images'),
        ),
    ]
