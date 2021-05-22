# Generated by Django 3.2.2 on 2021-05-14 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mgmt', '0003_productinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='mgmt.companyinfo'),
        ),
    ]