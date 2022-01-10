# Generated by Django 4.0 on 2022-01-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCredit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='cod',
        ),
        migrations.AddField(
            model_name='cart',
            name='prepaid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='prepaid',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]