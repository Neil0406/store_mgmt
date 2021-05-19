# Generated by Django 3.2.2 on 2021-05-17 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgmt', '0011_companyproductinfo_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinfo',
            name='color',
        ),
        migrations.AddField(
            model_name='productinfo',
            name='brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
