# Generated by Django 4.0 on 2022-01-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]