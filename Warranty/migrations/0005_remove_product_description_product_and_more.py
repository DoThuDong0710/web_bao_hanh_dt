# Generated by Django 5.0.4 on 2024-04-30 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Warranty', '0004_alter_product_warranty_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description_product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='fault_status',
        ),
        migrations.RemoveField(
            model_name='product',
            name='requires_repair',
        ),
        migrations.RemoveField(
            model_name='product',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='customer',
            name='address_customer',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty_product',
            field=models.IntegerField(blank=True, choices=[(0, 'Hết bảo hành'), (1, 'Còn bảo hành')], null=True),
        ),
    ]
