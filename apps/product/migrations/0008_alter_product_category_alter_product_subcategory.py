# Generated by Django 4.0 on 2021-12-18 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_product_discount_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='product.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(blank=True, to='product.SubCategory'),
        ),
    ]